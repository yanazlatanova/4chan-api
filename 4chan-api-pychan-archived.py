from pychan import FourChan, LogLevel, PychanLogger
from datetime import datetime, timezone
import json
import os

# Initialize pychan
logger = PychanLogger(LogLevel.INFO)
fourchan = FourChan(logger=logger, raise_http_exceptions=False)

# Simple keyword list
keywords = ["immigrants", "border", "refugees", "asylum", "migration", "illegal", "visa", "citizenship", "deportation"]

# Configuration
board = "pol"  # Board to search
max_threads = 800  # Limit threads to process (archived threads can be numerous)

# Create output directory
output_dir = "output_pychan_archived"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")

filtered_posts = []
total_posts = 0
total_threads = 0
archived_threads_processed = 0

print(f"Fetching archived threads from /{board}/...\n")
print("Note: This may take longer than live threads since we're processing archived content.\n")

try:
    for thread in fourchan.get_archived_threads(board):
        total_threads += 1
        archived_threads_processed += 1
        
        # Limit processing to avoid excessive runtime
        if archived_threads_processed > max_threads:
            print(f"Reached maximum thread limit ({max_threads}). Stopping...")
            break
            
        print(f"Processing archived thread #{archived_threads_processed}: {thread.title[:50]}..." if thread.title else f"Processing archived thread #{archived_threads_processed}")
        
        try:
            for post in fourchan.get_posts(thread):
                total_posts += 1
                
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
                        'thread_is_archived': post.thread.is_archived,
                        'post_number': post.number,
                        'post_url': post_url,
                        'timestamp': str(post.timestamp),
                        'poster_name': post.poster.name,
                        'poster_id': post.poster.id if post.poster.id else "No ID",
                        'poster_flag': post.poster.flag if post.poster.flag else "No Flag",
                        'text': post.text,
                        'matched_keywords': matched,
                        'is_original_post': post.is_original_post,
                        'has_file': post.file is not None,
                        'file_url': post.file.url if post.file else None,
                        'file_name': post.file.name if post.file else None
                    }
                    filtered_posts.append(post_data)
                    
                    print(f"✓ Match #{len(filtered_posts)}: {matched} in archived thread")
                    print(f"  Thread: {post.thread.title[:50] if post.thread.title else 'No title'}...")
                    print(f"  Text preview: {post.text[:100]}...\n")
        
        except Exception as e:
            print(f"Error processing thread {thread.number}: {e}")
            continue

except Exception as e:
    print(f"Error fetching archived threads: {e}")
    print("Note: Some boards (like /b/) don't have archives.")

print(f"\n{'='*80}")
print(f"ARCHIVED THREADS RESULTS:")
print(f"Total archived threads processed: {archived_threads_processed}")
print(f"Total posts checked: {total_posts}")
print(f"Posts with keywords: {len(filtered_posts)}")

if filtered_posts:
    # Save to JSON
    filename = os.path.join(output_dir, f'{board}_archived_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_posts, f, indent=2, ensure_ascii=False)
    
    # Save to readable text
    txt_filename = os.path.join(output_dir, f'{board}_archived_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(f"ARCHIVED THREADS ANALYSIS - /{board}/\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Keywords: {', '.join(keywords)}\n")
        f.write(f"Threads processed: {archived_threads_processed}\n")
        f.write(f"Total posts: {total_posts}\n")
        f.write(f"Matching posts: {len(filtered_posts)}\n")
        f.write(f"{'='*80}\n\n")
        
        for i, post in enumerate(filtered_posts, 1):
            f.write(f"\n{'='*80}\n")
            f.write(f"POST #{i} - Keywords: {', '.join(post['matched_keywords'])}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Thread: {post['thread_title']}\n")
            f.write(f"Thread #: {post['thread_number']} (Archived: {post['thread_is_archived']})\n")
            f.write(f"Time: {post['timestamp']}\n")
            f.write(f"Poster: {post['poster_name']}")
            if post['poster_id'] != "No ID":
                f.write(f" (ID: {post['poster_id']})")
            if post['poster_flag'] != "No Flag":
                f.write(f" ({post['poster_flag']})")
            f.write(f"\n")
            f.write(f"URL: {post['post_url']}\n")
            f.write(f"Original Post: {post['is_original_post']}\n")
            if post['has_file']:
                f.write(f"File: {post['file_name']} ({post['file_url']})\n")
            f.write(f"\n{post['text']}\n")
    
    print(f"\n✓ Saved to {filename}")
    print(f"✓ Saved readable version to {txt_filename}")
    
    # Show some statistics
    original_posts = sum(1 for post in filtered_posts if post['is_original_post'])
    posts_with_files = sum(1 for post in filtered_posts if post['has_file'])
    unique_threads = len(set(post['thread_number'] for post in filtered_posts))
    
    print(f"\n📊 Additional Statistics:")
    print(f"  Unique threads with matches: {unique_threads}")
    print(f"  Original posts (thread starters): {original_posts}")
    print(f"  Posts with files/images: {posts_with_files}")
    
else:
    print("\n✗ No matches found with current keywords in archived threads")
    print(f"Note: Only processed {archived_threads_processed} threads. Try increasing max_threads for more coverage.")

print(f"\n💡 Tip: Archived threads contain older discussions that may have more diverse content.")
print(f"Consider adjusting keywords or increasing max_threads for broader analysis.")