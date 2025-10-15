
# Vivaan Social Network Project

## Soical Netowrk App
_Create a Website for Cameron that meets his needs._

**Developer:** Vivaan Varma

---

## 1. Website Outline

### Project Description
A web forum where people can talk about **NBA games and players**. It is a safe space to talk about players and NBA games and is a welcoming community. This allows a website with a primary focus.

---

### Functional Requirements
- Users can **sign up** and **login**
- There is a **home page** with posts and recent news
- You can **create a post**
- **Share**, **comment**, and **like** posts

### Non-functional Requirements
- **Easy to use**
- **Safe and respectful environment**
- **Backed up data**

---

## 2. UI Design Plan

### Wireframe Sketches
Here is the basic layout of my app (sketched by hand):

**Home Page:**
![Wireframe Sketch](images/wireframe1.png)

**Posting Page:**
![Wireframe Sketch](images/wireframe2.png)

**Deep Dive into Posts:**
![Wireframe Sketch](images/wireframe3.png)

### Themes and Formatting

### Design Choices

| Element         | Choice                                                                 |
|----------------|------------------------------------------------------------------------|
| Colour Palette | Black, white, red – sporty and high contrast, matches NBA theme        |
| Typography     | Oswald for headings, Roboto for body – clean and easy to read          |
| Images/Icons   | NBA players, logos, court backgrounds. Font Awesome for like/share icons |

![Figma Wireframe](images/figmawire1.png)

---

## 3. Algorithms & Test Cases

### Login Page Algorithm
1. User opens the login page.
2. User enters username and password.
3. System checks if username exists in the database.
   - If NO → Display "User not found" message and stop.
4. If YES → Retrieve stored password for that username.
5. Compare entered password with stored password.
   - If match → Create session token and log user in. Redirect to dashboard/home page.
   - If no match → Display "Incorrect password" message and stop.

### Test Cases

| Test Case | Feature Tested | Preconditions | Steps | Expected Result |
|----------|---------------|---------------|-------|-----------------|
| Test 1   | Login with correct credentials | User account exists | 1. Go to login page<br>2. Enter correct username/password<br>3. Click "Login" | Redirect to dashboard |
| Test 2   | Login with wrong password      | User account exists | 1. Go to login page<br>2. Enter correct username/wrong password<br>3. Click "Login" | Display "Incorrect password" |

<img src="images/flowchart3.png" alt="Login Flowchart" width="800"/>

---

## 4. Weekly Progress & Features

### Week 5: SQL and Queries
This week, I created mock data and successfully imported it into VS Code using SQLite. I then wrote and tested several SQL queries on the dataset, which allowed me to retrieve and analyze useful information. Through this process, I learned how to manage data in a database environment and gained insights into how queries can be used to answer specific questions.

### Week 6-7: Making Webpages and Styling
This week, I created the homepage for the website and applied basic styling using HTML and CSS. The homepage layout was set up to match the planned design, and I experimented with colors and fonts to fit the NBA theme. This was my first step in building the user interface for the project.

### Week 8-9: Finishing Styling Home Pages
This week, I worked on styling and building the Games, Players, Profile, and Login pages for my app using HTML and CSS. The Games Page lets users view and predict upcoming NBA games, while the Players Page shows player stats with a filter option to search by name or team. The Profile Page displays user info and saved activity, and the Login Page allows users to securely sign in. I kept a consistent blue-and-white NBA-style theme across all pages and made sure they link smoothly. Overall, the site now has a clean, functional layout and feels much more complete.

### Week 10-11: Adding Interactivity
This week, I focused on adding interactivity and connecting the front end of my app to the backend. I created a working login system that connects to the database and stores user data securely. Users can now make posts that are saved in the backend and can also delete, comment, and like posts, which makes the app feel much more interactive and dynamic. I also implemented a filter system that lets users easily sort and view specific content, and this feature is fully connected to the backend as well.

---

## 5. Performance & Lighthouse Reports

In terms of performance, I ran a Lighthouse report and achieved an average score of 92 across all pages, which shows the site is well-optimized overall. The main area for improvement is offline compatibility, as the site currently relies on a network connection. Another point noted is that most of my images are linked from external websites rather than stored locally on my computer. I chose this approach because there are a large number of images, and linking them directly from the web keeps the project lighter and easier to manage. Overall, this week’s focus on backend connectivity and interactivity has made the app feel much more complete and functional and is why I got an 82 for the players page.

### Lighthouse Report Screenshots

**Homepage Lighthouse Report:**
![Homepage Lighthouse Report](./images/homepage.png)

**Games Page Lighthouse Report:**
![Games Page Lighthouse Report](images/gamespage.png)

**Players Page Lighthouse Report:**
![Players Page Lighthouse Report](images/playerspage.png)

---

## 6. Instructions

1. Open in VS Code and in the terminal type `python3 main.py` (Mac) or `python main.py` (Windows).
2. Hold command and click the IP address which should end in 5100.
3. Login using user: `vivaan.varma@education.nsw.gov.au` password: `hi123`
4. Use the website now by using the arrows to go back to the home page to allow you to go to different pages of my website.