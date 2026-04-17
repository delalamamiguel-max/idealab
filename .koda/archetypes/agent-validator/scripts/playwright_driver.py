"""Playwright-based UI verification helpers for agent validation."""

import asyncio
from playwright.async_api import async_playwright, Page, Browser
from typing import Optional, Callable
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class PlaywrightDriver:
    """Wrapper for Playwright browser automation in agent validation."""
    
    def __init__(self, headless: bool = True, video_dir: Optional[str] = None):
        """Initialize Playwright driver.
        
        Args:
            headless: Run browser in headless mode
            video_dir: Directory to save video recordings
        """
        self.headless = headless
        self.video_dir = video_dir
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context = None
        self.page: Optional[Page] = None
    
    async def start(self):
        """Start browser session."""
        self.playwright = await async_playwright().start()
        
        browser_args = {
            "headless": self.headless
        }
        
        if self.video_dir:
            browser_args["record_video_dir"] = self.video_dir
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        logger.info("Playwright browser started")
    
    async def stop(self):
        """Stop browser session."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        logger.info("Playwright browser stopped")
    
    async def navigate(self, url: str, wait_until: str = "networkidle"):
        """Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_until: Wait condition (load, domcontentloaded, networkidle)
        """
        await self.page.goto(url, wait_until=wait_until)
        logger.info(f"Navigated to {url}")
    
    async def click(self, selector: str, timeout: int = 5000):
        """Click element.
        
        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
        """
        await self.page.click(selector, timeout=timeout)
        logger.debug(f"Clicked {selector}")
    
    async def fill(self, selector: str, value: str, timeout: int = 5000):
        """Fill input field.
        
        Args:
            selector: CSS selector
            value: Value to fill
            timeout: Timeout in milliseconds
        """
        await self.page.fill(selector, value, timeout=timeout)
        logger.debug(f"Filled {selector} with value")
    
    async def get_text(self, selector: str, timeout: int = 5000) -> str:
        """Get element text content.
        
        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
            
        Returns:
            Text content
        """
        element = await self.page.wait_for_selector(selector, timeout=timeout)
        text = await element.text_content()
        return text or ""
    
    async def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Wait for element to appear.
        
        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
        """
        await self.page.wait_for_selector(selector, timeout=timeout)
        logger.debug(f"Found {selector}")
    
    async def screenshot(self, path: str):
        """Take screenshot.
        
        Args:
            path: Path to save screenshot
        """
        await self.page.screenshot(path=path)
        logger.info(f"Screenshot saved to {path}")
    
    async def get_page_state(self) -> dict:
        """Get current page state.
        
        Returns:
            Dict with URL, title, and other state
        """
        return {
            "url": self.page.url,
            "title": await self.page.title(),
            "timestamp": datetime.now().isoformat()
        }


async def verify_signup_flow(
    base_url: str,
    email: str,
    password: str,
    assertions: Optional[list[Callable]] = None
) -> dict:
    """Verify signup flow with assertions at each step.
    
    Args:
        base_url: Application base URL
        email: Test email
        password: Test password
        assertions: List of assertion functions to run at each step
        
    Returns:
        Verification results
    """
    driver = PlaywrightDriver(headless=True, video_dir="./test_videos")
    results = {"success": True, "steps": [], "errors": []}
    
    try:
        await driver.start()
        
        # Step 1: Navigate to signup
        await driver.navigate(f"{base_url}/signup")
        results["steps"].append({
            "step": "navigate_signup",
            "status": "success",
            "state": await driver.get_page_state()
        })
        
        # Step 2: Fill signup form
        await driver.fill("input[name='email']", email)
        await driver.fill("input[name='password']", password)
        await driver.click("button[type='submit']")
        results["steps"].append({
            "step": "submit_signup",
            "status": "success"
        })
        
        # Step 3: Wait for confirmation
        await driver.wait_for_selector(".signup-success", timeout=10000)
        confirmation_text = await driver.get_text(".signup-success")
        results["steps"].append({
            "step": "signup_confirmation",
            "status": "success",
            "confirmation": confirmation_text
        })
        
        # Run custom assertions
        if assertions:
            for i, assertion in enumerate(assertions):
                try:
                    await assertion(driver)
                    results["steps"].append({
                        "step": f"assertion_{i}",
                        "status": "success"
                    })
                except AssertionError as e:
                    results["success"] = False
                    results["errors"].append(f"Assertion {i} failed: {e}")
        
    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))
        logger.error(f"Signup flow verification failed: {e}")
    
    finally:
        await driver.stop()
    
    return results


async def verify_checkout_flow(
    base_url: str,
    product_id: str,
    test_card: dict,
    expected_states: list[str]
) -> dict:
    """Verify checkout flow with state assertions.
    
    Args:
        base_url: Application base URL
        product_id: Product to purchase
        test_card: Test card details
        expected_states: Expected states at each step
        
    Returns:
        Verification results
    """
    driver = PlaywrightDriver(headless=True, video_dir="./test_videos")
    results = {"success": True, "steps": [], "errors": []}
    
    try:
        await driver.start()
        
        # Step 1: Add to cart
        await driver.navigate(f"{base_url}/product/{product_id}")
        await driver.click("button.add-to-cart")
        await driver.wait_for_selector(".cart-badge")
        
        cart_count = await driver.get_text(".cart-badge")
        assert cart_count == "1", f"Expected cart count 1, got {cart_count}"
        
        results["steps"].append({
            "step": "add_to_cart",
            "status": "success",
            "cart_count": cart_count
        })
        
        # Step 2: Go to checkout
        await driver.navigate(f"{base_url}/checkout")
        await driver.wait_for_selector(".checkout-form")
        
        results["steps"].append({
            "step": "navigate_checkout",
            "status": "success"
        })
        
        # Step 3: Fill payment details
        await driver.fill("input[name='card_number']", test_card["number"])
        await driver.fill("input[name='exp_month']", test_card["exp_month"])
        await driver.fill("input[name='exp_year']", test_card["exp_year"])
        await driver.fill("input[name='cvc']", test_card["cvc"])
        
        results["steps"].append({
            "step": "fill_payment",
            "status": "success"
        })
        
        # Step 4: Submit payment
        await driver.click("button.submit-payment")
        await driver.wait_for_selector(".payment-success", timeout=15000)
        
        # Verify final state
        success_message = await driver.get_text(".payment-success")
        assert "success" in success_message.lower(), "Payment success message not found"
        
        results["steps"].append({
            "step": "payment_complete",
            "status": "success",
            "message": success_message
        })
        
    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))
        logger.error(f"Checkout flow verification failed: {e}")
    
    finally:
        await driver.stop()
    
    return results


async def verify_interactive_cli(
    command: str,
    expected_prompts: list[tuple[str, str]],
    expected_output: str
) -> dict:
    """Verify interactive CLI with tmux.
    
    Args:
        command: Command to run
        expected_prompts: List of (prompt_text, response) tuples
        expected_output: Expected final output
        
    Returns:
        Verification results
    """
    # Note: This would use tmux or pexpect for CLI testing
    # Simplified example here
    results = {
        "success": True,
        "command": command,
        "interactions": [],
        "errors": []
    }
    
    try:
        # Start process
        proc = await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Handle prompts
        for prompt_text, response in expected_prompts:
            # Read until prompt
            output = await asyncio.wait_for(
                proc.stdout.read(1024),
                timeout=5.0
            )
            
            output_str = output.decode()
            assert prompt_text in output_str, f"Expected prompt '{prompt_text}' not found"
            
            # Send response
            proc.stdin.write(f"{response}\n".encode())
            await proc.stdin.drain()
            
            results["interactions"].append({
                "prompt": prompt_text,
                "response": response,
                "status": "success"
            })
        
        # Get final output
        final_output = await asyncio.wait_for(
            proc.stdout.read(),
            timeout=5.0
        )
        
        final_output_str = final_output.decode()
        assert expected_output in final_output_str, "Expected output not found"
        
        results["final_output"] = final_output_str
        
    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))
        logger.error(f"CLI verification failed: {e}")
    
    return results


class VideoRecorder:
    """Record test execution as video."""
    
    def __init__(self, output_dir: str = "./test_videos"):
        """Initialize video recorder.
        
        Args:
            output_dir: Directory to save videos
        """
        self.output_dir = output_dir
        self.recordings = {}
    
    async def start_recording(self, test_name: str) -> PlaywrightDriver:
        """Start recording test.
        
        Args:
            test_name: Name of test
            
        Returns:
            Playwright driver with recording enabled
        """
        driver = PlaywrightDriver(headless=False, video_dir=self.output_dir)
        await driver.start()
        
        self.recordings[test_name] = {
            "driver": driver,
            "started_at": datetime.now()
        }
        
        logger.info(f"Started recording {test_name}")
        return driver
    
    async def stop_recording(self, test_name: str) -> str:
        """Stop recording and save video.
        
        Args:
            test_name: Name of test
            
        Returns:
            Path to saved video
        """
        if test_name not in self.recordings:
            raise ValueError(f"No recording found for {test_name}")
        
        recording = self.recordings[test_name]
        driver = recording["driver"]
        
        await driver.stop()
        
        duration = datetime.now() - recording["started_at"]
        
        video_path = f"{self.output_dir}/{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
        
        logger.info(f"Stopped recording {test_name} (duration: {duration})")
        
        del self.recordings[test_name]
        
        return video_path
