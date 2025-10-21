import requests
import json
from datetime import datetime, timezone, timedelta
import re
import os

# ============================================================================
# CONFIGURATION - MODIFY THESE SETTINGS
# ============================================================================

# Keywords to search for (case-insensitive)
KEYWORDS = ["trump", "election", "vote", "biden", "government", "president", "policy", "democrat", "republican"]

# Time range configuration
# NOTE: 4chan catalog only shows CURRENTLY ACTIVE threads
# You can only get posts that are still live on the board
# Older posts may not be available if threads were archived/deleted

# Option 1: Recent time ranges (recommended)
START_DATE = datetime.now(timezone.utc) - timedelta(hours=2)  # Last 2 hours
END_DATE = datetime.now(timezone.utc)

# Option 2: Specific recent dates (may return fewer results if threads are gone)
# START_DATE = datetime(2025, 10, 21, 0, 0, 0, tzinfo=timezone.utc)  # Oct 21, 2025 midnight
# END_DATE = datetime(2025, 10, 21, 23, 59, 59, tzinfo=timezone.utc)  # Oct 21, 2025 end of day

# Option 2: Relative time ranges (uncomment to use instead)
# START_DATE = datetime.now(timezone.utc) - timedelta(hours=24)  # Last 24 hours
# END_DATE = datetime.now(timezone.utc)

# Option 3: Last few hours (uncomment to use instead)
# START_DATE = datetime.now(timezone.utc) - timedelta(hours=6)  # Last 6 hours
# END_DATE = datetime.now(timezone.utc)

# Board to search (default: pol)
BOARD = "pol"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_html(text):
    """Remove HTML tags and decode entities from 4chan post text"""
    if not text:
        return ""
    
    # Remove HTML tags
    clean = re.sub(r'<[^<]+?>', '', text)
    
    # Decode common HTML entities
    clean = clean.replace('&gt;', '>')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&quot;', '"')
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&#039;', "'")
    clean = clean.replace('<br>', '\n')
    clean = clean.replace('<wbr>', '')
    
    # Clean up 4chan quote links (>>123456789>)
    clean = re.sub(r'>>\d+>', '', clean)  # Remove quote links like >>519431737>
    # like in "post_text": ">>519433413>We already know that people who didn't get the vaccine are more rural and unhealthier than those who did get the vaccineApproximately 6.5 million healthy young adults (ages 18-49) in Canada received at least one covid vaccine dose, based on 2023 national coverage rates of 75% across this group. That ESMO study getting all the media hype right now is totally bogus and cooked up on political orders, because the cancer-causing effects of gene therapy disguised as a \"covid vaccine\" are slowly breaking through to public awareness and thats a deadly threat to the murderers running governments.",

    
    # Clean up greentext arrows at start of lines
    clean = re.sub(r'^>+', '> ', clean, flags=re.MULTILINE)  # Normalize greentext
    
    # WHAT IS GREENTEXT?
    # Greentext is a distinctive 4chan posting style where lines starting with ">" appear in green color
    # Used for storytelling, quoting, implications, or emphasis. Common formats:
    # > be me                    (storytelling format)
    # > 22 years old
    # > decide to learn coding
    # > implying democracy works (sarcastic implications)
    # > Trump wins election      (listing points/events)
    # The regex above normalizes multiple arrows (>>>, >>>>) to single "> " for cleaner output
    
    return clean.strip()

def check_keywords(text, keywords):
    """Check if any keywords are present in the text (case-insensitive)"""
    if not text:
        return []
    
    text_lower = text.lower()
    matched = []
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched.append(keyword)
    
    return matched

def format_timestamp(unix_timestamp):
    """Convert Unix timestamp to readable format"""
    try:
        return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Unknown"

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def get_catalog(board):
    """Fetch the catalog for a specific board"""
    try:
        url = f"https://a.4cdn.org/{board}/catalog.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching catalog: {e}")
        return None

def get_thread_posts(board, thread_no):
    """Fetch all posts from a specific thread"""
    try:
        url = f"https://a.4cdn.org/{board}/thread/{thread_no}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching thread {thread_no}: {e}")
        return None

def filter_posts_by_time_and_keywords(board, start_date, end_date, keywords):
    """Main function to filter posts by time range and keywords"""
    
    print(f"Fetching posts from /{board}/...")
    print(f"Time range: {start_date.strftime('%Y-%m-%d %H:%M:%S')} to {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Keywords: {', '.join(keywords)}")
    print("WARNING: Only currently active threads are available via 4chan API")
    print("Older posts may not be found if their threads were archived/deleted")
    print("="*80)
    
    catalog = get_catalog(board)
    if not catalog:
        return []
    
    filtered_posts = []
    total_threads = 0
    checked_posts = 0
    
    # Convert datetime to Unix timestamps for comparison
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    # Go through each page in the catalog
    for page in catalog:
        for thread in page.get('threads', []):
            total_threads += 1
            thread_no = thread.get('no')
            
            # Check if the original post (OP) is in our time range
            thread_time = thread.get('time', 0)
            
            if start_timestamp <= thread_time <= end_timestamp:
                # Get the full thread to check all posts
                thread_data = get_thread_posts(board, thread_no)
                
                if thread_data and 'posts' in thread_data:
                    for post in thread_data['posts']:
                        checked_posts += 1
                        post_time = post.get('time', 0)
                        
                        # Check if post is in time range
                        if start_timestamp <= post_time <= end_timestamp:
                            # Clean and check post content
                            post_text = clean_html(post.get('com', ''))
                            thread_title = clean_html(post.get('sub', ''))
                            
                            # Combine title and text for keyword searching
                            full_text = f"{thread_title} {post_text}"
                            
                            # Check for keywords
                            matched_keywords = check_keywords(full_text, keywords)
                            
                            if matched_keywords:
                                post_data = {
                                    'board': board,
                                    'thread_no': thread_no,
                                    'post_no': post.get('no'),
                                    'thread_title': thread_title or "No Title",
                                    'post_text': post_text,
                                    'poster_name': post.get('name', 'Anonymous'),
                                    'poster_id': post.get('id', ''),
                                    'timestamp': post_time,
                                    'human_time': format_timestamp(post_time),
                                    'replies': post.get('replies', 0),
                                    'images': post.get('images', 0),
                                    'thread_url': f"https://boards.4chan.org/{board}/thread/{thread_no}",
                                    'post_url': f"https://boards.4chan.org/{board}/thread/{thread_no}#p{post.get('no')}",
                                    'matched_keywords': matched_keywords
                                }
                                
                                filtered_posts.append(post_data)
                                
                                print(f"✓ Match #{len(filtered_posts)}: {matched_keywords}")
                                print(f"  Thread: {post_data['thread_title'][:50]}...")
                                print(f"  Time: {post_data['human_time']}")
                                print(f"  Text preview: {post_text[:100]}...")
                                print()
    
    print("="*80)
    print(f"RESULTS:")
    print(f"Total threads checked: {total_threads}")
    print(f"Total posts checked: {checked_posts}")
    print(f"Posts matching criteria: {len(filtered_posts)}")
    
    return filtered_posts

def save_results(filtered_posts, board):
    """Save filtered posts to JSON and text files"""
    if not filtered_posts:
        print("\n✗ No matches found with current criteria")
        return
    
    # Create output directory
    output_dir = "output_official_api"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save to JSON
    json_filename = os.path.join(output_dir, f'{board}_filtered_raw_{timestamp}.json')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_posts, f, indent=2, ensure_ascii=False)
    
    # Save to readable text
    txt_filename = os.path.join(output_dir, f'{board}_filtered_raw_{timestamp}.txt')
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(f"4chan /{board}/ Filtered Posts\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Time Range: {START_DATE.strftime('%Y-%m-%d %H:%M:%S')} to {END_DATE.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Keywords: {', '.join(KEYWORDS)}\n")
        f.write(f"Total Matches: {len(filtered_posts)}\n")
        f.write("="*80 + "\n\n")
        
        for i, post in enumerate(filtered_posts, 1):
            f.write(f"POST #{i} - Keywords: {', '.join(post['matched_keywords'])}\n")
            f.write("="*80 + "\n")
            f.write(f"Thread: {post['thread_title']}\n")
            f.write(f"Time: {post['human_time']}\n")
            f.write(f"Poster: {post['poster_name']}")
            if post['poster_id']:
                f.write(f" (ID: {post['poster_id']})")
            f.write(f"\nURL: {post['post_url']}\n")
            f.write(f"Replies: {post['replies']}, Images: {post['images']}\n")
            f.write("-" * 40 + "\n")
            f.write(f"{post['post_text']}\n")
            f.write("\n" + "="*80 + "\n\n")
    
    print(f"\n✓ Saved {len(filtered_posts)} posts to:")
    print(f"  JSON: {json_filename}")
    print(f"  Text: {txt_filename}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("4chan API Raw Scraper")
    print("="*80)
    
    # Run the filtering
    results = filter_posts_by_time_and_keywords(BOARD, START_DATE, END_DATE, KEYWORDS)
    
    # Save results
    save_results(results, BOARD)
    
    print("\n✓ Script completed!")