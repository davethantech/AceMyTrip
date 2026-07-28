"""Browser Automation Service using Playwright for job search and applications."""

import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from src.shared.utils.config import get_settings

logger = structlog.get_logger()
settings = get_settings()


class JobSource:
    """Enumeration of supported job sources."""
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    REMOTE_OK = "remote_ok"
    WELLFOUND = "wellfound"
    OTTA = "otta"
    WE_WORK_REMOTELY = "weworkremotely"
    Y_COMBINATOR = "ycombinator"
    REMOTE_CO = "remote_co"
    COMPANY_PAGE = "company_page"


class BrowserAutomationService:
    """Service for browser automation using Playwright."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        logger.info("BrowserAutomationService initialized")
    
    async def start(self, headless: bool = True):
        """Start the browser instance."""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                ]
            )
            
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
            
            logger.info("Browser started successfully")
        except Exception as e:
            logger.error("Failed to start browser", error=str(e))
            raise
    
    async def close(self):
        """Close the browser instance."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("Browser closed")
    
    async def navigate(self, url: str, wait_until: str = "domcontentloaded"):
        """Navigate to a URL."""
        if not self.context:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.page = await self.context.new_page()
        await self.page.goto(url, wait_until=wait_until, timeout=30000)
        logger.info("Navigated to URL", url=url)
    
    async def screenshot(self, path: str) -> str:
        """Take a screenshot of the current page."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        await self.page.screenshot(path=path, full_page=True)
        logger.info("Screenshot taken", path=path)
        return path
    
    async def extract_text(self, selector: str) -> Optional[str]:
        """Extract text content from an element."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        try:
            element = await self.page.query_selector(selector)
            if element:
                return await element.text_content()
            return None
        except Exception as e:
            logger.warning("Failed to extract text", selector=selector, error=str(e))
            return None
    
    async def extract_all_text(self, selector: str) -> List[str]:
        """Extract text content from all matching elements."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        try:
            elements = await self.page.query_selector_all(selector)
            return [await el.text_content() for el in elements if el]
        except Exception as e:
            logger.warning("Failed to extract all text", selector=selector, error=str(e))
            return []
    
    async def click(self, selector: str, timeout: int = 5000):
        """Click an element."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        await self.page.click(selector, timeout=timeout)
        logger.info("Clicked element", selector=selector)
    
    async def fill(self, selector: str, value: str):
        """Fill a form field."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        await self.page.fill(selector, value)
        logger.info("Filled form field", selector=selector)
    
    async def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for an element to appear."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        await self.page.wait_for_selector(selector, timeout=timeout)
    
    async def get_page_content(self) -> str:
        """Get the full HTML content of the current page."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        return await self.page.content()
    
    async def evaluate(self, script: str) -> Any:
        """Execute JavaScript in the page context."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        return await self.page.evaluate(script)


class JobSearchAgent(BrowserAutomationService):
    """Agent for automated job searching across multiple platforms."""
    
    def __init__(self):
        super().__init__()
        self.search_results: List[Dict[str, Any]] = []
    
    async def search_linkedin(self, keywords: str, location: str = "Remote") -> List[Dict[str, Any]]:
        """Search jobs on LinkedIn."""
        jobs = []
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_WT=2"
            await self.navigate(url)
            
            # Wait for job listings to load
            await self.wait_for_selector(".job-search-card", timeout=15000)
            
            # Extract job cards
            job_cards = await self.extract_all_text(".job-search-card__title")
            companies = await self.extract_all_text(".job-search-card__company-name")
            locations = await self.extract_all_text(".job-search-card__location")
            
            for i, title in enumerate(job_cards[:20]):  # Limit to 20 jobs
                jobs.append({
                    "source": JobSource.LINKEDIN,
                    "title": title.strip() if title else "",
                    "company": companies[i].strip() if i < len(companies) else "",
                    "location": locations[i].strip() if i < len(locations) else "",
                    "url": f"https://www.linkedin.com/jobs/view/{i}",  # Placeholder
                    "scraped_at": datetime.utcnow().isoformat(),
                })
            
            logger.info("LinkedIn search completed", jobs_found=len(jobs))
        except Exception as e:
            logger.error("LinkedIn search failed", error=str(e))
        
        self.search_results.extend(jobs)
        return jobs
    
    async def search_indeed(self, keywords: str, location: str = "Remote") -> List[Dict[str, Any]]:
        """Search jobs on Indeed."""
        jobs = []
        try:
            url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&remotejob=1"
            await self.navigate(url)
            
            # Wait for job listings
            await self.wait_for_selector(".job_seenBeacon", timeout=15000)
            
            titles = await self.extract_all_text("h2.jobTitle span[title]")
            companies = await self.extract_all_text("span.companyName")
            
            for i, title in enumerate(titles[:20]):
                jobs.append({
                    "source": JobSource.INDEED,
                    "title": title.strip(),
                    "company": companies[i].strip() if i < len(companies) else "",
                    "location": location,
                    "url": f"https://www.indeed.com/viewjob?jk={i}",  # Placeholder
                    "scraped_at": datetime.utcnow().isoformat(),
                })
            
            logger.info("Indeed search completed", jobs_found=len(jobs))
        except Exception as e:
            logger.error("Indeed search failed", error=str(e))
        
        self.search_results.extend(jobs)
        return jobs
    
    async def search_remote_ok(self) -> List[Dict[str, Any]]:
        """Search jobs on RemoteOK."""
        jobs = []
        try:
            url = "https://remoteok.com/"
            await self.navigate(url)
            
            await self.wait_for_selector(".job", timeout=15000)
            
            job_elements = await self.page.query_selector_all(".job")[:20]
            
            for job_el in job_elements:
                title_el = await job_el.query_selector(".vertical-align-center h2")
                company_el = await job_el.query_selector(".vertical-align-center .company-link")
                
                title = await title_el.text_content() if title_el else ""
                company = await company_el.text_content() if company_el else ""
                
                jobs.append({
                    "source": JobSource.REMOTE_OK,
                    "title": title.strip(),
                    "company": company.strip(),
                    "location": "Remote",
                    "url": "https://remoteok.com/job",  # Placeholder
                    "scraped_at": datetime.utcnow().isoformat(),
                })
            
            logger.info("RemoteOK search completed", jobs_found=len(jobs))
        except Exception as e:
            logger.error("RemoteOK search failed", error=str(e))
        
        self.search_results.extend(jobs)
        return jobs
    
    async def search_wellfound(self, keywords: str) -> List[Dict[str, Any]]:
        """Search jobs on Wellfound (formerly AngelList)."""
        jobs = []
        try:
            url = f"https://wellfound.com/jobs?query={keywords}&remote=true"
            await self.navigate(url)
            
            await self.wait_for_selector("[data-test-id='feed-section']", timeout=15000)
            
            titles = await self.extract_all_text("[data-test-id='job-title']")
            companies = await self.extract_all_text("[data-test-id='job-company']")
            
            for i, title in enumerate(titles[:20]):
                jobs.append({
                    "source": JobSource.WELLFOUND,
                    "title": title.strip(),
                    "company": companies[i].strip() if i < len(companies) else "",
                    "location": "Remote",
                    "url": "https://wellfound.com/job",  # Placeholder
                    "scraped_at": datetime.utcnow().isoformat(),
                })
            
            logger.info("Wellfound search completed", jobs_found=len(jobs))
        except Exception as e:
            logger.error("Wellfound search failed", error=str(e))
        
        self.search_results.extend(jobs)
        return jobs
    
    async def comprehensive_search(
        self, 
        keywords: str, 
        location: str = "Remote",
        sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Perform comprehensive job search across multiple sources."""
        if sources is None:
            sources = ["linkedin", "indeed", "remote_ok", "wellfound"]
        
        all_jobs = []
        
        await self.start(headless=settings.PLAYWRIGHT_HEADLESS)
        
        try:
            if "linkedin" in sources:
                jobs = await self.search_linkedin(keywords, location)
                all_jobs.extend(jobs)
            
            if "indeed" in sources:
                jobs = await self.search_indeed(keywords, location)
                all_jobs.extend(jobs)
            
            if "remote_ok" in sources:
                jobs = await self.search_remote_ok()
                all_jobs.extend(jobs)
            
            if "wellfound" in sources:
                jobs = await self.search_wellfound(keywords)
                all_jobs.extend(jobs)
            
            # Remove duplicates based on title + company
            unique_jobs = []
            seen = set()
            for job in all_jobs:
                key = f"{job['title']}_{job['company']}_{job['source']}"
                if key not in seen:
                    seen.add(key)
                    unique_jobs.append(job)
            
            logger.info("Comprehensive search completed", total_jobs=len(unique_jobs))
            return unique_jobs
        
        finally:
            await self.close()


class ApplicationAssistant(BrowserAutomationService):
    """Assistant for helping with job applications."""
    
    def __init__(self):
        super().__init__()
        self.application_logs: List[Dict[str, Any]] = []
    
    async def prepare_application_form(self, job_url: str) -> Dict[str, Any]:
        """Navigate to application form and analyze required fields."""
        await self.start(headless=False)  # Interactive mode for user review
        
        try:
            await self.navigate(job_url)
            
            # Take screenshot for user review
            screenshot_path = f"/tmp/application_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
            await self.screenshot(screenshot_path)
            
            # Analyze form fields
            form_fields = await self.evaluate("""
                () => {
                    const inputs = document.querySelectorAll('input, textarea, select');
                    return Array.from(inputs).map(el => ({
                        type: el.type || el.tagName.toLowerCase(),
                        name: el.name || el.id || '',
                        placeholder: el.placeholder || '',
                        required: el.required || false,
                        label: el.previousElementSibling?.textContent?.trim() || ''
                    }));
                }
            """)
            
            # Find submit button
            submit_button = await self.evaluate("""
                () => {
                    const buttons = document.querySelectorAll('button, input[type="submit"]');
                    for (const btn of buttons) {
                        if (btn.textContent.toLowerCase().includes('submit') || 
                            btn.textContent.toLowerCase().includes('apply')) {
                            return { text: btn.textContent.trim(), selector: btn.id || btn.className };
                        }
                    }
                    return null;
                }
            """)
            
            result = {
                "screenshot_path": screenshot_path,
                "form_fields": form_fields,
                "submit_button": submit_button,
                "ready_for_review": True,
            }
            
            logger.info("Application form prepared", url=job_url)
            return result
        
        except Exception as e:
            logger.error("Failed to prepare application form", error=str(e))
            raise
        finally:
            await self.close()
    
    async def autofill_application(
        self,
        user_data: Dict[str, Any],
        approval_required: bool = True
    ) -> Dict[str, Any]:
        """Autofill application form with user data (requires approval)."""
        if not self.page:
            raise RuntimeError("No page loaded. Call prepare_application_form first.")
        
        filled_fields = []
        skipped_fields = []
        
        # Map common field names to user data
        field_mapping = {
            "email": user_data.get("email"),
            "phone": user_data.get("phone"),
            "name": user_data.get("full_name"),
            "firstName": user_data.get("first_name"),
            "lastName": user_data.get("last_name"),
            "linkedin": user_data.get("linkedin_url"),
            "website": user_data.get("website"),
            "resume": user_data.get("resume_path"),
        }
        
        for field_name, value in field_mapping.items():
            if value:
                try:
                    # Try different selector strategies
                    selectors = [
                        f'input[name="{field_name}"]',
                        f'input[id="{field_name}"]',
                        f'input[placeholder*="{field_name}" i]',
                        f'label:has-text("{field_name}") + input',
                    ]
                    
                    for selector in selectors:
                        try:
                            await self.wait_for_selector(selector, timeout=2000)
                            if field_name == "resume":
                                # Handle file upload
                                await self.page.set_input_files(selector, value)
                            else:
                                await self.fill(selector, str(value))
                            filled_fields.append(field_name)
                            break
                        except:
                            continue
                
                except Exception as e:
                    skipped_fields.append({"field": field_name, "reason": str(e)})
        
        result = {
            "filled_fields": filled_fields,
            "skipped_fields": skipped_fields,
            "requires_approval": approval_required,
            "message": "Form filled. Please review before submitting." if approval_required else "Form filled successfully.",
        }
        
        logger.info("Application autofilled", filled=len(filled_fields), skipped=len(skipped_fields))
        return result
    
    async def capture_application_proof(self) -> Dict[str, Any]:
        """Capture proof of application submission."""
        if not self.page:
            raise RuntimeError("No page loaded.")
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        # Take screenshot
        screenshot_path = f"/tmp/application_proof_{timestamp}.png"
        await self.screenshot(screenshot_path)
        
        # Get current URL
        current_url = self.page.url
        
        # Get page title
        page_title = await self.page.title()
        
        proof = {
            "screenshot_path": screenshot_path,
            "url": current_url,
            "page_title": page_title,
            "timestamp": timestamp,
        }
        
        self.application_logs.append(proof)
        logger.info("Application proof captured", path=screenshot_path)
        return proof
