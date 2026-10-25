"""Static guardrails for the Android source; NOT an APK compilation test."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / 'app/src/main/java/com/btcaud/paper'

class SourceContract(unittest.TestCase):
    def test_manifest_has_no_trading_or_foreground_service(self):
        root = ET.parse(ROOT / 'app/src/main/AndroidManifest.xml').getroot()
        self.assertFalse(root.findall('.//service'))
        self.assertEqual(2, len(root.findall('.//receiver[@android:exported="true"]', {'android': 'http://schemas.android.com/apk/res/android'})))
        self.assertNotIn('FOREGROUND_SERVICE', (ROOT / 'app/src/main/AndroidManifest.xml').read_text())

    def test_only_public_kraken_endpoint(self):
        text = (JAVA / 'network/KrakenPublicFeed.kt').read_text()
        self.assertIn('https://api.kraken.com/0/public/OHLC', text)
        self.assertNotIn('/private/', text)
        self.assertNotIn('AddOrder', text)
        self.assertIn('if (nowS - start < 14_400L) continue', text)

    def test_refill_is_audited_and_deposits_not_profit(self):
        core = (JAVA / 'core/PaperModel.kt').read_text()
        db = (JAVA / 'data/PaperDatabase.kt').read_text()
        self.assertIn('cumulativeFundingCents', core)
        self.assertIn('Math.subtractExact(cashCents, cumulativeFundingCents)', core)
        self.assertIn('funding_audit', db)
        self.assertIn('db.beginTransaction()', db)

    def test_widgets_and_background_job(self):
        manifest = (ROOT / 'app/src/main/AndroidManifest.xml').read_text()
        self.assertIn('ToggleWidgetReceiver', manifest)
        self.assertIn('DashboardWidgetReceiver', manifest)
        scheduler = (JAVA / 'work/WorkScheduler.kt').read_text()
        self.assertIn('PeriodicWorkRequestBuilder<MarketSyncWorker>(15, TimeUnit.MINUTES)', scheduler)
        self.assertIn('NetworkType.CONNECTED', scheduler)
        toggle = (JAVA / 'widgets/ToggleWidget.kt').read_text()
        self.assertIn('class PauseAction', toggle)
        self.assertIn('class ResumeAction', toggle)
        self.assertIn('AppControl.setEnabled(context, false)', toggle)
        self.assertIn('AppControl.setEnabled(context, true)', toggle)

    def test_purple_notification_and_no_live_trading(self):
        notif = (JAVA / 'notifications/StatusNotification.kt').read_text()
        self.assertIn('Color.rgb(124, 58, 237)', notif)
        worker = (JAVA / 'work/MarketSyncWorker.kt').read_text()
        self.assertIn('KrakenPublicFeed.fetchCompleted', worker)
        self.assertNotIn('placeOrder', worker)
        self.assertNotIn('trade', worker.lower().split('/**')[0])

if __name__ == '__main__': unittest.main()
