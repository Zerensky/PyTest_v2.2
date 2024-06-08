import pytest
import requests
from ddt import ddt, data, unpack
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@ddt
class TestPosts:

    @data(
        ("Post Title 1"),
        ("Post Title 2"),
        ("Post Title 3")
    )
    @unpack
    def test_check_post_title(self, auth_token, config, post_title):
        headers = {
            "X-Auth-Token": auth_token
        }
        response = requests.get(f"{config['site_url']}/api/posts", headers=headers, params={"owner": "notMe"})
        response.raise_for_status()
        
        posts = response.json()
        post_titles = [post['title'] for post in posts]
        
        assert post_title in post_titles, f"Post with title '{post_title}' not found."
    
    def test_create_and_check_post(self, auth_token, config):
        headers = {
            "X-Auth-Token": auth_token,
            "Content-Type": "application/json"
        }
        post_data = {
            "title": "Test Post",
            "description": "This is a test post",
            "content": "Test post content"
        }

        # Create a new post
        create_response = requests.post(f"{config['site_url']}/api/posts", headers=headers, json=post_data)
        create_response.raise_for_status()

        # Check if the post exists
        check_response = requests.get(f"{config['site_url']}/api/posts", headers=headers, params={"owner": "me"})
        check_response.raise_for_status()
        
        posts = check_response.json()
        post_descriptions = [post['description'] for post in posts]
        
        assert post_data['description'] in post_descriptions, f"Post with description '{post_data['description']}' not found."
    
    def test_successful_login(self, config):
        login_url = f"{config['site_url']}/gateway/login"
        response = requests.post(login_url, data={
            "username": config['username'],
            "password": config['password']
        })
        response.raise_for_status()
        assert response.status_code == 200, "Login failed"
    
    def test_add_post_via_ui(self, browser, config):
        login_url = config['login_url']
        site_url = config['site_url']
        
        # Open login page
        browser.get(login_url)
        
        # Enter username and password
        browser.find_element(By.NAME, "username").send_keys(config['username'])
        browser.find_element(By.NAME, "password").send_keys(config['password'])
        
        # Click login button
        browser.find_element(By.XPATH, "//button[text()='Login']").click()
        
        # Wait for the login to complete and the user to be redirected
        WebDriverWait(browser, 10).until(EC.url_contains(site_url))
        
        # Navigate to the post creation page
        browser.find_element(By.XPATH, "//a[text()='Create Post']").click()
        
        # Wait for the post creation page to load
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "title")))
        
        # Enter post details
        post_title = "Test Post UI"
        post_description = "This is a test post created via UI"
        post_content = "Test post content via UI"
        
        browser.find_element(By.NAME, "title").send_keys(post_title)
        browser.find_element(By.NAME, "description").send_keys(post_description)
        browser.find_element(By.NAME, "content").send_keys(post_content)
        
        # Click create post button
        browser.find_element(By.XPATH, "//button[text()='Create']").click()
        
        # Wait for the post to be created and user to be redirected
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, f"//h2[text()='{post_title}']")))
        
        # Check if the post is present on the page
        assert browser.find_element(By.XPATH, f"//h2[text()='{post_title}']").is_displayed(), "Post not found on the page"
    
    def test_contact_us_form(self, browser, config):
        login_url = config['login_url']
        site_url = config['site_url']
        
        # Open login page
        browser.get(login_url)
        
        # Enter username and password
        browser.find_element(By.NAME, "username").send_keys(config['username'])
        browser.find_element(By.NAME, "password").send_keys(config['password'])
        
        # Click login button
        browser.find_element(By.XPATH, "//button[text()='Login']").click()
        
        # Wait for the login to complete and the user to be redirected
        WebDriverWait(browser, 10).until(EC.url_contains(site_url))
        
        # Navigate to the Contact Us form
        browser.find_element(By.XPATH, "//a[text()='Contact Us']").click()
        
        # Wait for the Contact Us form to load
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "contact-email")))
        
        # Enter form details
        contact_email = "test@example.com"
        contact_subject = "Test Subject"
        contact_message = "This is a test message."
        
        browser.find_element(By.NAME, "contact-email").send_keys(contact_email)
        browser.find_element(By.NAME, "contact-subject").send_keys(contact_subject)
        browser.find_element(By.NAME, "contact-message").send_keys(contact_message)
        
        # Click the submit button
        browser.find_element(By.XPATH, "//button[text()='Send']").click()
        
        # Wait for the alert to appear
        WebDriverWait(browser, 10).until(EC.alert_is_present())
        
        # Switch to the alert
        alert = browser.switch_to.alert
        
        # Print and verify the alert text
        alert_text = alert.text
        print(alert_text)
        assert "Message sent successfully" in alert_text, "Alert text does not match expected text"
        
        # Accept the alert
        alert.accept()
