from datetime import datetime
import math
from . import FeedSource

SECONDS_PER_DAY = 60 * 60 * 24

class Norm(FeedSource):

    def _norn_feed(self, amplitude, reference_timestamp, current_timestamp, period, phase_offset):
	    """
	    Given the reference timestamp, the current timestamp, the period (in days), the phase (in days), the reference asset value (ie 1.00) and the amplitude (> 0 && < 1), output the current value.
	    """
	    waveform = math.sin(((((current_timestamp - (reference_timestamp + phase_offset))/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.
	    return 1 + (amplitude * waveform)
    
    def _fetch(self):
        feed = {}

        reference_timestamp = datetime.strptime("2015-10-13T14:12:24", "%Y-%m-%dT%H:%M:%S").timestamp() # Bitshares 2.0 genesis block timestamp
        current_timestamp = datetime.now().timestamp() # Current timestamp for reference within the script
        amplitude = 0.12612612612
        period = SECONDS_PER_DAY * 28

        urthr_value = self._norn_feed(
            amplitude,
            reference_timestamp,
            current_timestamp,
            period,
            SECONDS_PER_DAY * 0 # phase offset
            )
        self.add_rate(feed, 'BTS', 'URTHR', urthr_value, 1.0)

        verthandi_value = self._norn_feed(
            amplitude,
            reference_timestamp,
            current_timestamp,
            period,
            SECONDS_PER_DAY * 9.33 # phase offset
            )
        self.add_rate(feed, 'BTS', 'VERTHANDI', verthandi_value, 1.0)

        skuld_value = self._norn_feed(
            amplitude,
            reference_timestamp,
            current_timestamp,
            period,
            SECONDS_PER_DAY * 18.66 # phase offset
            )
        self.add_rate(feed, 'BTS', 'SKULD', skuld_value, 1.0)

        return feed
