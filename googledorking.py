import requests
from bs4 import BeautifulSoup
import csv
import time

# Categories with Sensitive Dorks for Google Dorking
categories = {
    'Personal Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"login"',
        'site:{} inurl:"userprofile" inurl:"password"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"api_key"',
        'site:{} inurl:"secret"',
        'site:{} inurl:"config.php"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} inurl:"/config/database.php"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} inurl:"token"',
        'site:{} inurl:"auth"',
        'site:{} inurl:"database"',
        'site:{} inurl:".env"',
        'site:{} inurl:"/upload"',
        'site:{} inurl:"/files/"',
        'site:{} "db_password"',
        'site:{} "access token"',
        'site:{} "db_host"',
        'site:{} "mysql password"',
        'site:{} inurl:"secrets.json"',
        'site:{} inurl:"config.json"',
        'site:{} "AWS credentials"',
        'site:{} "secret key"',
        'site:{} "API secret"',
        'site:{} "private key"'
    ],
    'Business Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"login"',
        'site:{} inurl:"/admin"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"api_key"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} inurl:"config.php"',
        'site:{} inurl:"/config/database.php"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} inurl:"auth"',
        'site:{} inurl:"token"',
        'site:{} inurl:"/uploads"',
        'site:{} inurl:"api_secret"',
        'site:{} inurl:"database"',
        'site:{} inurl:"db_password"',
        'site:{} "db_host"',
        'site:{} "API key"',
        'site:{} inurl:"confidential"',
        'site:{} "token"',
        'site:{} "private key"',
        'site:{} "secret key"',
        'site:{} inurl:"secrets.json"',
        'site:{} "AWS credentials"',
        'site:{} "service account key"',
        'site:{} "docker secrets"',
        'site:{} "server credentials"'
    ],
    'Educational Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"login"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} inurl:"/config/database.php"',
        'site:{} "student_password"',
        'site:{} inurl:"/admin"',
        'site:{} inurl:"token"',
        'site:{} inurl:"auth"',
        'site:{} inurl:"secrets.json"',
        'site:{} "db_password"',
        'site:{} "API key"',
        'site:{} "database"',
        'site:{} "student portal"',
        'site:{} "faculty login"',
        'site:{} "user credentials"',
        'site:{} "access token"',
        'site:{} "private key"',
        'site:{} inurl:"config.json"',
        'site:{} "AWS credentials"',
        'site:{} "admin password"',
        'site:{} inurl:"confidential"',
        'site:{} "server secrets"',
        'site:{} "db_host"',
        'site:{} inurl:"exam_results"'
    ],
    'News and Media Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"api_key"',
        'site:{} "confidential"',
        'site:{} inurl:"db_password"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} "private_key"',
        'site:{} inurl:"token"',
        'site:{} "server credentials"',
        'site:{} inurl:"config/database.php"',
        'site:{} "AWS credentials"',
        'site:{} "auth_token"',
        'site:{} inurl:"access_token"',
        'site:{} "api_secret"',
        'site:{} inurl:"/uploads"',
        'site:{} "secrets.json"',
        'site:{} inurl:".env"',
        'site:{} inurl:"config.json"',
        'site:{} "db_host"',
        'site:{} inurl:"/admin/config"',
        'site:{} "private data"',
        'site:{} inurl:"confidential"',
        'site:{} "api_secret"',
        'site:{} inurl:"/.git"',
        'site:{} "auth_key"'
    ],
    'Social Media Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"login"',
        'site:{} inurl:"credentials"',
        'site:{} "user data"',
        'site:{} inurl:"auth_token"',
        'site:{} inurl:"API key"',
        'site:{} "session_id"',
        'site:{} inurl:"secret"',
        'site:{} inurl:"config.json"',
        'site:{} "user_profile"',
        'site:{} inurl:"passwords"',
        'site:{} "access_token"',
        'site:{} "db_password"',
        'site:{} "AWS credentials"',
        'site:{} inurl:"database"',
        'site:{} "private key"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} "social media API key"',
        'site:{} inurl:"confidential"',
        'site:{} "API secret"',
        'site:{} inurl:"db_host"',
        'site:{} "server_key"',
        'site:{} inurl:"/.env"',
        'site:{} "private data"',
        'site:{} "confidential data"'
    ],
    'Nonprofit and Charity Websites': [
        'site:{} inurl:"donate" inurl:"password"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"api_key"',
        'site:{} "confidential"',
        'site:{} "donor_information"',
        'site:{} inurl:"admin" inurl:"token"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} inurl:"secrets.json"',
        'site:{} inurl:"confidential_data"',
        'site:{} "AWS credentials"',
        'site:{} "private key"',
        'site:{} inurl:"/uploads"',
        'site:{} inurl:"passwords"',
        'site:{} "api_secret"',
        'site:{} inurl:"database"',
        'site:{} "db_password"',
        'site:{} inurl:"secrets"',
        'site:{} "access_token"',
        'site:{} "API key"',
        'site:{} inurl:"donation details"',
        'site:{} inurl:"donor_data"',
        'site:{} "server credentials"',
        'site:{} inurl:"donation_id"',
        'site:{} inurl:"user_profile"',
        'site:{} inurl:"/.env"'
    ],
    'Government Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"admin" inurl:"password"',
        'site:{} inurl:"credentials"',
        'site:{} inurl:"/config/database.php"',
        'site:{} "confidential"',
        'site:{} "government sensitive"',
        'site:{} inurl:"api_key"',
        'site:{} "admin password"',
        'site:{} inurl:"token"',
        'site:{} "secret key"',
        'site:{} "access_token"',
        'site:{} inurl:"/.env"',
        'site:{} "database"',
        'site:{} "AWS credentials"',
        'site:{} "private key"',
        'site:{} inurl:"public-services"',
        'site:{} inurl:"citizen-data"',
        'site:{} inurl:"official-docs"',
        'site:{} "govt credentials"',
        'site:{} "data leak"',
        'site:{} "server secrets"',
        'site:{} inurl:"confidential"',
        'site:{} inurl:"secrets.json"',
        'site:{} inurl:"/wp-config.php"'
    ],
    'Health and Wellness Websites': [
        'site:{} inurl:"password"',
        'site:{} inurl:"login"',
        'site:{} inurl:"/wp-config.php"',
        'site:{} "medical data"',
        'site:{} inurl:"credentials"',
        'site:{} "patient information"',
        'site:{} inurl:"confidential"',
        'site:{} inurl:"API key"',
        'site:{} inurl:"auth_token"',
        'site:{} inurl:"database"',
        'site:{} "db_password"',
        'site:{} inurl:"/uploads"',
        'site:{} "confidential data"',
        'site:{} inurl:"patient-credentials"',
        'site:{} "medical secrets"',
        'site:{} inurl:"secret"',
        'site:{} "health data leak"',
        'site:{} "access token"',
        'site:{} "health records"',
        'site:{} inurl:"/.env"',
        'site:{} "user secrets"',
        'site:{} "API secret"',
        'site:{} inurl:"medications"'
    ]
}

# Function to prompt user for website input and return the dork results
def generate_dorks_for_website():
    website = input("Enter the website URL (without 'http://'): ")
    
    # Prompt user to select category
    print("\nSelect the category for dorking:")
    for idx, category in enumerate(categories.keys(), start=1):
        print(f"{idx}. {category}")
    
    category_choice = int(input("\nEnter the number of your selected category: ")) - 1
    selected_category = list(categories.keys())[category_choice]
    
    # Generate dorks for selected category
    print(f"\nSelected Category: {selected_category}\n")
    
    for dork in categories[selected_category]:
        query = dork.format(website)
        print(f"Running query: {query}")
        
        # Send request to Google search engine using dork (simulated here)
        url = f"https://www.google.com/search?q={query}"
        
        # Simulating the result fetching
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h3')
        
        # Display results
        for result in results:
            print(f"Found result: {result.text}")
        
        time.sleep(2)  # Avoid overwhelming the server with requests

# Run the dorking
generate_dorks_for_website()
