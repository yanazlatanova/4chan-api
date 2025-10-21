from pychan import FourChan, LogLevel, PychanLogger
from datetime import datetime, timezone
import json

# Initialize pychan
logger = PychanLogger(LogLevel.INFO)
fourchan = FourChan(logger=logger, raise_http_exceptions=False)

# Simple keyword list
keywords = ["trump", "election", "vote", "biden", "government", "president", "policy", "democrat", "republican"]

# Just get posts from today
start_date = datetime(2025, 10, 20, tzinfo=timezone.utc)
end_date = datetime(2025, 10, 21, tzinfo=timezone.utc)

filtered_posts = []
total_posts = 0
posts_today = 0

print("Fetching posts from /pol/...\n")

for thread in fourchan.get_threads("pol"):
    try:
        for post in fourchan.get_posts(thread):
            total_posts += 1
            
            # Check if post is from today
            if post.timestamp >= start_date and post.timestamp < end_date:
                posts_today += 1
                
                # Convert to lowercase for matching
                text_lower = post.text.lower()
                
                # Check each keyword
                matched = []
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        matched.append(keyword)
                
                # If we found matches, save the post
                if matched:
                    # Build URLs manually
                    thread_url = f"https://boards.4chan.org/{post.thread.board}/thread/{post.thread.number}"
                    post_url = f"https://boards.4chan.org/{post.thread.board}/thread/{post.thread.number}#p{post.number}"
                    
                    post_data = {
                        'thread_title': post.thread.title if post.thread.title else "No Title",
                        'thread_board': post.thread.board,
                        'thread_number': post.thread.number,
                        'thread_url': thread_url,
                        'post_number': post.number,
                        'post_url': post_url,
                        'timestamp': str(post.timestamp),
                        'poster_name': post.poster.name,
                        'text': post.text,
                        'matched_keywords': matched
                    }
                    filtered_posts.append(post_data)
                    
                    print(f"✓ Match #{len(filtered_posts)}: {matched}")
                    print(f"  Text preview: {post.text[:150]}...\n")
    
    except Exception as e:
        print(f"Error: {e}")
        continue

print(f"\n{'='*80}")
print(f"RESULTS:")
print(f"Total posts checked: {total_posts}")
print(f"Posts from Oct 20: {posts_today}")
print(f"Posts with keywords: {len(filtered_posts)}")

if filtered_posts:
    # Save to JSON
    filename = f'pol_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_posts, f, indent=2, ensure_ascii=False)
    
    # Save to readable text
    txt_filename = f'pol_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for i, post in enumerate(filtered_posts, 1):
            f.write(f"\n{'='*80}\n")
            f.write(f"POST #{i} - Keywords: {', '.join(post['matched_keywords'])}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Thread: {post['thread_title']}\n")
            f.write(f"Time: {post['timestamp']}\n")
            f.write(f"Poster: {post['poster_name']}\n")
            f.write(f"URL: {post['post_url']}\n")
            f.write(f"\n{post['text']}\n")
    
    print(f"\n✓ Saved to {filename}")
    print(f"✓ Saved readable version to {txt_filename}")
else:
    print("\n✗ No matches found with current keywords")
    print(f"\nTry running the script for longer to check more posts")