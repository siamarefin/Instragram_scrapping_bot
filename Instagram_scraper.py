import instaloader
import csv
import getpass
import os
import time

# Function to scrape followers data (with resuming capability)
def scrape_followers_data(username, password, target_usernames):
    # Create an Instaloader instance
    L = instaloader.Instaloader()

    # Log in to your Instagram account
    L.login(username, password)

    for target_username in target_usernames:
        csv_filename = f"{target_username}_followers.csv"

        # Check if the file already exists to avoid duplicate entries
        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                # Write header only if the file is new
                writer.writerow([
                    'Profile Username', 'Profile Full Name', 'Profile Followers', 'Profile Following', 'Profile Post Count',
                    'Follower Username', 'Follower Full Name', 'Follower Followers', 'Follower Following', 'Follower Post Count', 
                    'Follower ID', 'Follower Profile Link', 'Follower Biography'
                ])

            try:
                # Load profile
                print(f"Trying to load profile: {target_username}")
                profile = instaloader.Profile.from_username(L.context, target_username)
                print(f"Profile loaded successfully for {target_username}")

                # Get the profile data
                profile_full_name = profile.full_name if profile.full_name else "N/A"
                profile_followers = profile.followers
                profile_following = profile.followees
                profile_post_count = profile.mediacount

                # Scraping followers in batches (500 at a time)
                follower_count = profile.followers
                print(f"Scraping up to {follower_count} followers of {target_username}")

                # Retrieve previously scraped followers to avoid duplicates
                scraped_followers = set()
                if file_exists:
                    with open(csv_filename, 'r', encoding='utf-8') as existing_file:
                        reader = csv.reader(existing_file)
                        next(reader)  # Skip header
                        for row in reader:
                            if len(row) > 6:
                                scraped_followers.add(row[5])  # Collect already scraped follower usernames

                count = 0  # Count how many followers are scraped in this session

                # Scrape followers with pause to avoid rate limits
                for follower in profile.get_followers():
                    follower_username = follower.username
                    follower_full_name = follower.full_name if follower.full_name else "N/A"

                    # Avoid duplicates by checking previously scraped followers
                    if follower_username not in scraped_followers:
                        try:
                            follower_followers = follower.followers
                            follower_following = follower.followees
                            follower_post_count = follower.mediacount
                            follower_id = follower.userid  # Follower's unique ID
                            follower_profile_link = f"https://www.instagram.com/{follower_username}/"  # Follower profile link
                            follower_biography = follower.biography if follower.biography else "N/A"  # Follower's biography
                        except Exception as e:
                            follower_followers = "N/A"
                            follower_following = "N/A"
                            follower_post_count = "N/A"
                            follower_id = "N/A"
                            follower_profile_link = "N/A"
                            follower_biography = "N/A"
                            print(f"Could not load additional info for follower {follower_username}: {e}")

                        # Write the profile data with each follower's data
                        writer.writerow([
                            target_username, profile_full_name, profile_followers, profile_following, profile_post_count,
                            follower_username, follower_full_name, follower_followers, follower_following, follower_post_count,
                            follower_id, follower_profile_link, follower_biography
                        ])
                        print(f"Scraped follower: {follower_username} ({follower_full_name}) - ID: {follower_id}, Link: {follower_profile_link}, Bio: {follower_biography}")
                        count += 1
                    else:
                        print(f"Skipping already scraped follower: {follower_username}")

                    # Stop after 500 followers per session to avoid rate limit, then resume later
                    if count >= 500:
                        print(f"Reached limit of 500 followers scraped for {target_username} in this session.")
                        break

                print(f"Finished scraping {count} followers for {target_username}.")

                # Add a sleep to avoid Instagram rate limits
                time.sleep(60)  # 1 minute pause after each profile

            except Exception as e:
                print(f"Error while scraping followers of {target_username}: {e}")

# Main function to execute the script
if __name__ == '__main__':
    username = "siamarefin2"
    password = "siamarefiN@6761"
    # target_usernames_input = input("Enter the usernames to scrape (comma separated): ")
    target_usernames_input = "artbasel"
    target_usernames = [username.strip() for username in target_usernames_input.split(',')]

    # Scrape followers data (with resuming capability and 500 followers per session)
    scrape_followers_data(username, password, target_usernames)