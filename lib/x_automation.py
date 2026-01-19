"""X (Twitter) app automation."""

from time import sleep


class XAutomation:
    """Automates interactions with X (Twitter) app."""

    def __init__(self, device):
        self.device = device

    def open_x_app(self):
        """Open the X app by clicking on the app icon."""
        try:
            self.device.xpath('//*[@content-desc="X"]').click()
            sleep(3)
            print("Opened X app")
            return True
        except Exception as e:
            print(f"Failed to open X app: {e}")
            return False

    def open_composer(self):
        """Open the tweet composer by clicking the compose button."""
        try:
            # Click composer button twice (sometimes needed for UI response)
            self.device.xpath(
                '//*[@resource-id="com.twitter.android:id/composer_write"]'
            ).click()
            sleep(1)
            self.device.xpath(
                '//*[@resource-id="com.twitter.android:id/composer_write"]'
            ).click()
            sleep(2)
            print("Opened composer")
            return True
        except Exception as e:
            print(f"Failed to open composer: {e}")
            return False

    def write_and_post_tweet(self, text: str):
        """Write tweet text and post it."""
        try:
            # Click text input area
            self.device.click(180, 500)
            sleep(1)

            # Set tweet text
            self.device.set_fastinput_ime(True)
            self.device.send_keys(text)
            self.device.set_fastinput_ime(False)
            print(f"Wrote tweet: {text}")
            sleep(1)

            # Click post button
            self.device.click(928, 192)
            print("Clicked post button")
            sleep(5)
            return True
        except Exception as e:
            print(f"Failed to write/post tweet: {e}")
            return False
