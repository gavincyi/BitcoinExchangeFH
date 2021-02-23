import logging
from datetime import datetime
import re

from cryptofeed import FeedHandler
from cryptofeed.defines import L2_BOOK, TRADES, BID, ASK
from cryptofeed.callback import BookCallback, TradeCallback
import cryptofeed.exchanges as cryptofeed_exchanges

from .rest_api_exchange import RestApiExchange

LOGGER = logging.getLogger(__name__)

FULL_UTC_PATTERN = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z'


class WebsocketExchange(RestApiExchange):
    """Websocket exchange.
    """

    def __init__(self, **kwargs):
        """Constructor.
        """
        super().__init__(**kwargs)
        self._feed_handler = None
        self._instrument_mapping = None

    def load(self, **kwargs):
        """Load.
        """
        super().load(is_initialize_instmt=False, **kwargs)
        self._feed_handler = FeedHandler()
        self._instrument_mapping = self._create_instrument_mapping()
        try:
            exchange = getattr(
                cryptofeed_exchanges,
                self._get_exchange_name(self._name))
        except AttributeError as e:
            raise ImportError(
                'Cannot load exchange %s from websocket' % self._name)

        if self._is_orders:                       
            channels = [TRADES, L2_BOOK]            
            callbacks = {
                TRADES: TradeCallback(self._update_trade_callback),
                L2_BOOK: BookCallback(self._update_order_book_callback)               
            }            
        else:
            channels = [TRADES]
            callbacks = {
                TRADES: TradeCallback(self._update_trade_callback),                
            }            

        if self._name.lower() == 'poloniex':
            self._feed_handler.add_feed(
                exchange(
                    channels=list(self._instrument_mapping.keys()),
                    callbacks=callbacks))
        else:
            self._feed_handler.add_feed(
                exchange(
                    symbols=list(self._instrument_mapping.keys()),
                    channels=channels,
                    callbacks=callbacks))

    def run(self):
        """Run.
        """
        self._feed_handler.run()

    @staticmethod
    def _get_exchange_name(name):
        """Get exchange name.
        """
        if name == 'Hitbtc':
            return 'HitBTC'
        elif name == 'Okex':
            return "OKEx"
        elif name == "HuobiPro":
            return "Huobi"

        return name

    def _create_instrument_mapping(self):
        """Create instrument mapping.
        """
        mapping = {}
        instruments_notin_ccxt = {'UST/USD':'UST-USD'}
        for name in self._instruments.keys():
            if self._name.lower() == 'bitmex' or self._type == 'futures' or self._type == 'swap':
                # BitMEX uses the instrument name directly
                # without normalizing to cryptofeed convention
                if name.find(':')>=0:
                    # name with : like HuobiDM
                    names = name.split(':')
                    normalized_name = names[0]
                    name = names[1]
                else:
                    normalized_name = name
            elif name in instruments_notin_ccxt.keys():
                normalized_name = instruments_notin_ccxt[name]
            else:

                market = self._exchange_interface.markets[name]
                normalized_name = market['base'] + '-' + market['quote']
            mapping[normalized_name] = name

        return mapping

    def _update_order_book_callback(self, feed, pair, book, timestamp, receipt_timestamp):
        """Update order book callback.
        """
        instrument_key = self._get_instrument_key(feed, pair)
            
        instmt_info = self._instruments[instrument_key]
        
        is_updated = instmt_info.websocket_update_bids_asks(
            bids=book[BID],
            asks=book[ASK])

        if not is_updated:
            return
        

    def _update_trade_callback(
            self, feed, pair, order_id, timestamp, side, amount, price, receipt_timestamp):
        """Update trade callback.
        """
        instrument_key = self._get_instrument_key(feed, pair)
            
        instmt_info = self._instruments[instrument_key]
        trade = {}

        if isinstance(timestamp, str):
            if (len(timestamp) == 27 and
                    re.search(FULL_UTC_PATTERN, timestamp) is not None):
                timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                timestamp = timestamp.timestamp()
                trade['timestamp'] = timestamp
            else:
                trade['timestamp'] = float(timestamp)
        else:
            trade['timestamp'] = timestamp

        trade['id'] = order_id
        trade['price'] = float(price)
        trade['amount'] = float(amount)

        current_timestamp = datetime.utcnow()

        if not instmt_info.update_trade(trade, current_timestamp):
            return

        for handler in self._handlers.values():
            instmt_info.update_table(handler=handler)

        self._rotate_ordre_tables()

    def _check_valid_instrument(self):
        """Check valid instrument.
        """
        skip_checking_exchanges = ['bitmex', 'bitfinex', 'okex']
        if self._name.lower() in skip_checking_exchanges:
            # Skip checking on BitMEX
            # Skip checking on Bitfinex
            return

        for instrument_code in self._config['instruments']:
            if instrument_code not in self._exchange_interface.markets:
                raise RuntimeError(
                    'Instrument %s is not found in exchange %s',
                    instrument_code, self._name)
            
            
    def _get_instrument_key(self, feed, pair):
        
        instruments_check_map_value = ['HUOBI_DM']
        if feed in instruments_check_map_value:
            for k,v in self._instrument_mapping.items():
                if pair == v:
                    instrument_key = k + ':' + v
                    break
        else:
            instrument_key = self._instrument_mapping[pair]  
            
        return instrument_key
