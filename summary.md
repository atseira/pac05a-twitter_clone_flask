Backend (Flask):
Directory Structure:
```
YourFlaskApp/
├── models/
│   ├── __init__.py
│   └── models.py       # Contains 'is_admin' attribute in User model
├── admin/
│   ├── __init__.py
│   └── admin_views.py  # Restricts admin access based on 'is_admin' attribute
├── api/
│   ├── __init__.py
│   └── resources.py    # Handles like/unlike, fetches tweets with pagination
├── templates/
│   └── login.html      # Login template for Flask-Admin interface
├── app.py              # Main application setup and initialization
├── init_db.py          # Script to initialize the database
└── reset_db.py         # Script to reset the database
```
Key Points:
- models.py: Introduced 'is_admin' attribute in User model to denote administrative privileges.
- admin_views.py: Ensures only users with 'is_admin' set to True can access Flask-Admin interface.
- resources.py: Implements tweet fetching with pagination, and like/unlike operations, computing 'liked' status for each tweet for current user.

Frontend (Vue.js):
Directory Structure:
```
YourVueApp/
├── src/
│   ├── components/
│   │   ├── TweetList.vue      # Displays tweets, updates like count in real-time
│   │   ├── LoginForm.vue      # Beautified login form
│   │   └── PostTweetForm.vue  # Beautified tweet post form
│   ├── store/
│   │   └── index.js            # Contains Pinia store setup
│   ├── App.vue                # Main component with enhanced navbar
│   ├── main.js                # Entry point for Vue application
│   └── router.js              # Vue Router for frontend routing
├── public/
│   └── index.html
├── styles/
│   └── styles.css             # Contains TailwindCSS styling
├── package.json               # Dependencies and scripts
└── vue.config.js              # Vue CLI configuration
```
Key Points:
- TweetList.vue: Displays tweets, allows users to toggle likes, and updates like count dynamically. Reflects 'liked' status of tweets for logged-in user.
- LoginForm.vue & PostTweetForm.vue: Beautified forms using Tailwind CSS.
- store/index.js: Manages state including user authentication and tweets using Pinia store.
- styles/styles.css: TailwindCSS for a consistent and responsive design.

Functionality:
- Real-time updates of like counts.
- Admin access is restricted to users with administrative privileges.
- UI improvements with Tailwind CSS for a seamless and responsive experience.
- 'Liked' status of tweets is accurately reflected for logged-in users.
- Pagination: Tweets are fetched and displayed in paginated form ensuring efficient data retrieval and display.
