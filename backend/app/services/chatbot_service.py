"""
Chatbot Service - AI-Powered Quiz Bot
Handles quiz sessions with AI-generated questions from Groq LLM
"""
from typing import List, Optional, Dict, Any
import os
import json
from dotenv import load_dotenv
from groq import Groq
import PyPDF2
import io

# Load environment variables
load_dotenv()


class ChatbotService:
    """Service for AI-powered quiz bot using Groq LLM"""
    
    # Fallback topics if AI generation fails
    FALLBACK_TOPICS = ["Python Programming", "Data Science", "Web Development", "Cloud Computing", "React", "Databases"]
    
    def __init__(self):
        # Store quiz sessions per chat
        self.quiz_sessions: Dict[str, Dict[str, Any]] = {}
        # Store PDF content per chat
        self.pdf_content: Dict[str, str] = {}
        
        # Initialize Groq client
        self.groq_client = None
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.groq_client = Groq(api_key=api_key)
    
    async def get_suggested_topics(self, user_chat_history: Optional[List[Dict[str, str]]] = None) -> List[str]:
        """
        Generate AI-powered topic suggestions based on actual user demand
        
        Args:
            user_chat_history: List of recent user chats with 'title' and 'created_at' fields
            
        Returns:
            List of exactly 6 topics for balanced UI grid (2 rows x 3 columns)
        """
        if not self.groq_client:
            # Fallback to default topics if Groq not available
            return self.FALLBACK_TOPICS
        
        try:
            # Prepare chat history context
            if user_chat_history and len(user_chat_history) > 0:
                # Format chat titles for the prompt
                chat_titles = "\n".join([f"- {chat.get('title', 'Untitled')}" for chat in user_chat_history])
                chat_context = f"""
User chat data (recent chat titles):
{chat_titles}
"""
            else:
                # No user data available, use generic prompt
                chat_context = "No user chat history available. Generate trending topics for 2026."

            prompt = f"""Based on the following user chat data, generate a list of EXACTLY 6 "Most Requested Topics".

Rules:
- Generate EXACTLY 6 topics (no more, no less) for balanced UI grid layout
- Topics must reflect actual user demand and frequency
- Merge similar topics into a single clear topic
- Keep topic names short and professional (2-4 words each)
- Do not include explanations
- Do not include numbering or emojis
- Output ONLY a JSON array of exactly 6 strings

User chat data:
{chat_context}

Example output format (EXACTLY 6 topics):
[
  "Data Science Interviews",
  "Machine Learning Projects",
  "Python Programming",
  "SQL Query Optimization",
  "Cloud Computing",
  "Web Development"
]

Generate the JSON array with EXACTLY 6 topics now:"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a data analyst that analyzes user behavior and generates topic trends. Always respond with valid JSON array only, no extra text."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON array from response
            # Handle cases where the model might add markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON response
            topics = json.loads(content)
            
            # Validate that we got a list of strings
            if isinstance(topics, list) and all(isinstance(t, str) for t in topics):
                # Ensure exactly 6 topics for balanced UI
                if len(topics) >= 6:
                    return topics[:6]
                elif len(topics) > 0:
                    # If AI returned fewer topics, pad with fallback topics
                    remaining = 6 - len(topics)
                    topics.extend(self.FALLBACK_TOPICS[:remaining])
                    return topics[:6]
                else:
                    return self.FALLBACK_TOPICS
            else:
                print(f"Invalid topic format from AI: {topics}")
                return self.FALLBACK_TOPICS
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {content}")
            return self.FALLBACK_TOPICS
        except Exception as e:
            print(f"Error generating topic suggestions: {e}")
            return self.FALLBACK_TOPICS
    
    def extract_pdf_text(self, pdf_file: bytes) -> str:
        """Extract text content from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def save_pdf_content(self, chat_id: str, content: str) -> None:
        """Save extracted PDF content for a chat session"""
        self.pdf_content[chat_id] = content
    
    def get_pdf_content(self, chat_id: str) -> Optional[str]:
        """Get saved PDF content for a chat session"""
        return self.pdf_content.get(chat_id)
    
    def remove_pdf_content(self, chat_id: str) -> bool:
        """Remove PDF content for a chat session"""
        if chat_id in self.pdf_content:
            del self.pdf_content[chat_id]
            return True
        return False
    
    async def _generate_quiz_questions(self, topic: str, num_questions: int = 5, pdf_content: Optional[str] = None, asked_questions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Generate quiz questions using Groq LLM"""
        if not self.groq_client:
            print("[ERROR] Groq client not initialized")
            return []
        
        # Try up to 2 times if first attempt fails
        for attempt in range(2):
            try:
                import time
                # Add timestamp to ensure unique questions each time
                seed = int(time.time() * 1000) % 10000
                
                # Build list of previously asked questions
                previous_questions_text = ""
                if asked_questions and len(asked_questions) > 0:
                    previous_questions_text = "\n\n**IMPORTANT - DO NOT REPEAT THESE QUESTIONS:**\n"
                    previous_questions_text += "\n".join([f"- {q}" for q in asked_questions[-10:]])  # Last 10 questions
                    previous_questions_text += "\n\nYou MUST generate COMPLETELY DIFFERENT questions that are NOT similar to any of the above.\n"
                
                # Enhance topic descriptions for better LLM understanding
                topic_enhancements = {
                    'python': 'Python programming (syntax, functions, classes, data structures, algorithms, OOP concepts, libraries like pandas/numpy, coding best practices)',
                    'data science': 'Data Science and AI (machine learning algorithms, pandas, numpy, statistics, data analysis, neural networks, scikit-learn)',
                    'web development': 'Web Development (HTML, CSS, JavaScript, REST APIs, web frameworks, responsive design, frontend/backend)',
                    'cloud computing': 'Cloud Computing (AWS, Azure, GCP, serverless architecture, containers, Docker, Kubernetes, cloud services)',
                    'react': 'React.js framework (hooks, components, state management, JSX, props, lifecycle, Next.js, TypeScript with React)',
                    'databases': 'Databases and SQL (relational databases, SQL queries, NoSQL databases, database design, normalization, optimization, indexes)'
                }
                
                # Use enhanced description if available, otherwise use the topic as-is
                enhanced_topic = topic_enhancements.get(topic.lower(), topic)
                
                # Build prompt based on PDF content availability
                if pdf_content:
                    prompt = f"""Generate exactly {num_questions} UNIQUE and DIVERSE multiple-choice quiz questions based on the following PDF content:

{pdf_content[:3000]}...
{previous_questions_text}

IMPORTANT REQUIREMENTS:
- Generate questions ONLY from the provided PDF content
- Make each question completely different and unique
- Use varied question styles and difficulty levels
- Cover different aspects of the content
- Each question must have 4 options (A, B, C, D)
- Only ONE option should be correct
- Include the correct answer letter

Return ONLY a JSON array in this EXACT format:
[
  {{{{
    "q": "Question text here?",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "a": "A"
  }}}}
]

Number of questions: {num_questions}
Uniqueness seed: {seed}

Generate {num_questions} varied, creative multiple-choice questions now. Return ONLY the JSON array, no other text."""
                else:
                    # Create diverse question areas for better variety
                    question_areas = []
                    if 'apple' in topic.lower() or 'fruit' in topic.lower():
                        question_areas = [
                            "nutritional value and health benefits",
                            "varieties and types",
                            "cultivation and growing conditions",
                            "history and origin",
                            "culinary uses and recipes"
                        ]
                    elif 'python' in topic.lower():
                        question_areas = [
                            "basic syntax and data types",
                            "functions and control flow",
                            "object-oriented programming",
                            "popular libraries (pandas, numpy, etc.)",
                            "best practices and common patterns"
                        ]
                    else:
                        question_areas = [
                            "fundamental concepts",
                            "practical applications",
                            "advanced topics",
                            "common use cases",
                            "best practices"
                        ]
                    
                    areas_instruction = "\n".join([f"  {i+1}. {area}" for i, area in enumerate(question_areas)])
                    
                    prompt = f"""Generate exactly {num_questions} COMPLETELY DIFFERENT multiple-choice quiz questions about {enhanced_topic}.
{previous_questions_text}

CRITICAL - QUESTION DIVERSITY RULES:
- Each question MUST cover a DIFFERENT aspect or concept
- NO two questions should ask about the same thing
- Distribute questions across these areas:
{areas_instruction}
- Vary the difficulty: mix easy, medium, and challenging questions
- Use different question formats (definition, application, comparison, analysis)

TOPIC FOCUS:
- ALL questions must be about {topic.upper()} ONLY
- Stay strictly on topic - do not mix in other subjects

FORMATTING REQUIREMENTS:
- Each question must have exactly 4 options (A, B, C, D)
- Only ONE option should be correct per question
- Make wrong options plausible but clearly incorrect
- Include the correct answer letter

Return ONLY a JSON array in this EXACT format:
[
  {{{{
    "q": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "a": "A"
  }}}}
]

Generate {num_questions} DIVERSE questions about DIFFERENT aspects of {enhanced_topic}. Return ONLY the JSON array."""

                print(f"[DEBUG] Attempt {attempt + 1} - Generating {num_questions} questions for topic: {topic}")
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an expert quiz generator. Your specialty is creating DIVERSE questions that cover DIFFERENT aspects of a topic. Each question you generate must be about a completely different concept or aspect. NEVER repeat similar questions. Return ONLY valid JSON format."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=1.1,  # Higher temperature for more variety
                    max_tokens=2048,
                    top_p=0.95,
                )
                
                content = response.choices[0].message.content.strip()
                
                print(f"[DEBUG] Raw AI response length: {len(content)}")
                print(f"[DEBUG] First 300 chars: {content[:300]}")
                
                # Extract JSON from response
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                questions = json.loads(content)
                
                print(f"[DEBUG] Parsed {len(questions) if isinstance(questions, list) else 0} questions")
                
                # Validate structure for MCQ format
                if isinstance(questions, list) and len(questions) > 0:
                    valid_questions = []
                    for idx, q in enumerate(questions):
                        if (isinstance(q, dict) and 
                            'q' in q and 
                            'options' in q and 
                            'a' in q and
                            isinstance(q.get('options'), list) and
                            len(q.get('options', [])) == 4):
                            valid_questions.append(q)
                        else:
                            print(f"[DEBUG] Question {idx} failed validation: {q}")
                    
                    if len(valid_questions) > 0:
                        print(f"[DEBUG] Successfully generated {len(valid_questions)} valid questions")
                        return valid_questions[:num_questions]
                
                print(f"[DEBUG] Attempt {attempt + 1} failed - retrying...")
                    
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON parsing error on attempt {attempt + 1}: {e}")
                if attempt == 0:
                    continue  # Retry
                return []
            except Exception as e:
                print(f"[ERROR] Error generating questions on attempt {attempt + 1}: {e}")
                if attempt == 0:
                    continue  # Retry
                return []
        
        print("[ERROR] All attempts failed to generate questions")
        return []
    
    async def generate_response(
        self, 
        message: str, 
        history: Optional[List] = None,
        chat_id: str = "",
        db_service = None,
        last_question_msg_id: str = None
    ) -> str:
        """
        Generate bot response based on user message
        
        Args:
            message: User's message
            history: Chat history (not used in quiz mode)
            chat_id: Chat ID for session tracking
            db_service: Database service for updating messages
            last_question_msg_id: ID of the last question message
            
        Returns:
            str: Bot response
        """
        message_lower = message.lower().strip()
        
        # Flexible quiz detection - check for various quiz-related keywords
        quiz_keywords = ['quiz', 'test', 'learn', 'teach', 'practice', 'study', 'questions about', 'ask me about']
        
        # Check if any quiz keyword is in the message
        is_quiz_request = any(keyword in message_lower for keyword in quiz_keywords)
        
        # If user requests a new quiz while one is active, terminate the old one
        if is_quiz_request and chat_id in self.quiz_sessions:
            # Extract topic from the new request
            topic = message_lower
            for phrase in ['quiz', 'test me on', 'teach me', 'teach me about', 'i want to learn', 
                          'learn about', 'practice', 'study', 'questions about', 'questions on',
                          'ask me about', 'ask me', 'give me', 'start', 'begin', 'on', 'about']:
                topic = topic.replace(phrase, ' ')
            topic = topic.strip()
            
            if topic:
                # Get previous quiz stats
                old_session = self.quiz_sessions[chat_id]
                old_topic = old_session.get('topic', 'unknown')
                old_score = old_session.get('score', 0)
                old_answered = old_session.get('answered', 0)
                
                # Get display name
                old_topic_display = old_session.get('topic_display', old_topic)
                
                # Terminate previous quiz
                del self.quiz_sessions[chat_id]
                
                # Start new quiz
                new_quiz = await self.start_quiz(chat_id, topic)
                return f"**Previous Quiz Terminated**\n\nTopic: {old_topic_display}\nScore: {old_score}/{old_answered} questions answered\n\n---\n\n{new_quiz}"
        
        # Check if user wants to remove PDF
        if message_lower in ['remove pdf', 'delete pdf', 'clear pdf']:
            if self.remove_pdf_content(chat_id):
                return "✅ PDF content has been removed. You can now upload a new PDF or start topic-based quizzes."
            else:
                return "ℹ️ No PDF content found to remove."
        
        # Check if user is in an active quiz session
        if chat_id in self.quiz_sessions:
            # Check if user wants to stop the quiz
            if message_lower == 'stop':
                return self._end_quiz(chat_id)
            
            # Check answer
            return await self.check_answer(chat_id, message, db_service, last_question_msg_id)
        
        if is_quiz_request:
            # Extract topic from the message
            topic = message_lower
            
            # Remove common quiz-related phrases to extract the topic
            for phrase in ['quiz', 'test me on', 'teach me', 'teach me about', 'i want to learn', 
                          'learn about', 'practice', 'study', 'questions about', 'questions on',
                          'ask me about', 'ask me', 'give me', 'start', 'begin', 'on', 'about']:
                topic = topic.replace(phrase, ' ')
            
            topic = topic.strip()
            
            # If we extracted a topic, start quiz
            if topic:
                return await self.start_quiz(chat_id, topic)
        
        # Default help message
        topics = ", ".join(self.FALLBACK_TOPICS)
        return f"""👋 Welcome to QuizBot - Your Learning Companion!

I help you learn through interactive quizzes with AI-generated questions. Here's how to get started:

📚 **Popular Topics:**
{topics}

💡 **How to Start:**
Just ask naturally! Examples: 
  • quiz python
  • test me on machine learning
  • teach me about biology
  • I want to learn world war 2
  • ask me questions about chemistry

📎 **Upload PDF:**
You can also upload any PDF document and type 'quiz pdf' to generate questions from it!
To remove uploaded PDF, type: 'remove pdf'

🎯 **How it Works:**
1. I'll generate fresh questions for you
2. Answer each question one by one
3. Get instant feedback
4. See your final score!

Ready to learn? Type 'quiz' followed by any topic you want to learn about! 🚀"""
    
    async def start_quiz(self, chat_id: str, topic: str) -> str:
        """Start a new quiz session with AI-generated questions"""
        topic_lower = topic.lower()
        
        print(f"[START QUIZ] chat_id: {chat_id}, topic: {topic_lower}")
        print(f"[START QUIZ] PDF content keys: {list(self.pdf_content.keys())}")
        
        # Check if PDF content exists for this chat
        pdf_content = self.get_pdf_content(chat_id)
        
        print(f"[START QUIZ] PDF content found: {pdf_content is not None}, length: {len(pdf_content) if pdf_content else 0}")
        
        # If user wants PDF quiz, check if PDF is uploaded
        if topic_lower == "pdf":
            if not pdf_content:
                return "📄 No PDF uploaded yet. Please upload a PDF file first using the 📎 button, then type 'quiz pdf'."
        
        if not self.groq_client:
            return "⚠️ AI service is not configured. Please set GROQ_API_KEY environment variable."
        
        # Initialize session for continuous quiz (no fixed question count)
        self.quiz_sessions[chat_id] = {
            "topic": topic_lower,
            "topic_display": topic,  # Store original user input for display
            "score": 0,
            "answered": 0,
            "current_question": None,
            "use_pdf": (topic_lower == "pdf"),  # Only use PDF if topic is explicitly 'pdf'
            "asked_questions": []  # Track previously asked questions to avoid repeats
        }
        
        # Generate and show first question
        return await self._ask_next_question(chat_id)
    
    async def _ask_next_question(self, chat_id: str) -> str:
        """Generate and ask the next question on demand"""
        session = self.quiz_sessions.get(chat_id)
        if not session:
            return "No active quiz. Type 'quiz [topic]' to start!"
        
        # Only use PDF content if this quiz is explicitly for PDF
        pdf_content = None
        if session.get("use_pdf", False):
            pdf_content = self.get_pdf_content(chat_id)
        
        # Get list of previously asked questions to avoid repeats
        asked_questions = session.get("asked_questions", [])
        
        # Generate a single new question with context of previous questions
        questions = await self._generate_quiz_questions(
            session["topic"], 
            num_questions=1, 
            pdf_content=pdf_content,
            asked_questions=asked_questions
        )
        
        if not questions or len(questions) == 0:
            return "Sorry, I couldn't generate a new question. Type 'stop' to end the quiz."
        
        question = questions[0]
        session["current_question"] = question
        
        # Store the question text to avoid repeating it
        session["asked_questions"].append(question['q'])
        
        progress = f"Question {session['answered'] + 1}"
        
        # Use the original user-typed topic name for display
        display_name = session.get('topic_display', session['topic'])
        
        # Format question with multiple choice options
        options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
        
        # Include correct answer as hidden data for frontend instant validation
        correct_answer = question.get('a', 'A').upper()
        
        return f"**{display_name} Assessment**\n{progress}\n\n{question['q']}\n\n{options_text}\n\nType your answer (A, B, C, or D) or 'stop' to end:\n[CORRECT:{correct_answer}]"
    
    async def check_answer(self, chat_id: str, user_answer: str, db_service=None, last_question_msg_id: str = None) -> str:
        """Check user's answer and generate next question"""
        session = self.quiz_sessions.get(chat_id)
        if not session:
            return "No active quiz. Type 'quiz [topic]' to start a quiz!"
        
        # Check if user wants to stop
        if user_answer.lower().strip() == 'stop':
            return self._end_quiz(chat_id)
        
        question = session.get("current_question")
        if not question:
            return "No active question. Something went wrong."
        
        correct_answer = question["a"].upper().strip()
        user_answer_clean = user_answer.upper().strip()
        
        # Check if answer is correct (accept just letter or full option text)
        is_correct = user_answer_clean == correct_answer
        
        if is_correct:
            session["score"] += 1
        
        session["answered"] += 1
        
        # Update the question message in database with markers
        if db_service and last_question_msg_id:
            question_msg = await db_service.get_message(last_question_msg_id)
            if question_msg:
                lines = question_msg.content.split('\n')
                updated_lines = []
                
                for line in lines:
                    # Check if line is an option (A. B. C. or D.)
                    stripped = line.strip()
                    if stripped and len(stripped) > 2 and stripped[0] in ['A', 'B', 'C', 'D'] and stripped[1] == '.':
                        option_letter = stripped[0]
                        if option_letter == correct_answer:
                            updated_lines.append(f"✅ {line}")
                        elif option_letter == user_answer_clean and not is_correct:
                            updated_lines.append(f"❌ {line}")
                        else:
                            updated_lines.append(line)
                    else:
                        updated_lines.append(line)
                
                # Add feedback message at the end
                updated_lines.append("")
                if is_correct:
                    updated_lines.append("✅ Correct!")
                else:
                    # Get the full text of the correct answer
                    correct_option_text = ""
                    for line in lines:
                        stripped = line.strip()
                        if stripped and len(stripped) > 2 and stripped[0] == correct_answer and stripped[1] == '.':
                            # Extract just the answer text after "X. "
                            correct_option_text = stripped[3:].strip() if len(stripped) > 3 else ""
                            break
                    
                    updated_lines.append(f"❌ Incorrect. The correct answer is {correct_answer}.")
                
                updated_content = '\n'.join(updated_lines)
                print(f"[DEBUG] Updating message {last_question_msg_id} with content:")
                print(f"[DEBUG] {updated_content}")
                await db_service.update_message_content(last_question_msg_id, updated_content)
        
        # Prepare feedback
        if is_correct:
            feedback = f"FEEDBACK:CORRECT:{correct_answer}"
        else:
            feedback = f"FEEDBACK:INCORRECT:{user_answer_clean}:{correct_answer}"
        
        # Generate next question automatically
        next_question = await self._ask_next_question(chat_id)
        feedback += f"\n\nNEXT_QUESTION:{next_question}"
        
        return feedback
    
    def _end_quiz(self, chat_id: str) -> str:
        """End quiz and show results"""
        session = self.quiz_sessions.get(chat_id)
        if not session:
            return "No quiz found."
        
        score = session["score"]
        total = session["answered"]
        percentage = (score / total * 100) if total > 0 else 0
        
        # Performance message based on percentage
        if percentage >= 80:
            performance = "Outstanding! Excellent work!"
        elif percentage >= 60:
            performance = "Good job! Keep it up!"
        elif percentage >= 40:
            performance = "Not bad! Practice makes perfect!"
        else:
            performance = "Keep learning! You'll get better!"
        
        # Clean up session
        topic = session["topic"]
        del self.quiz_sessions[chat_id]
        
        return f"""**Quiz Complete!**

**Your Score:** {score}/{total} ({percentage:.0f}%)

{performance}

Want to try again or explore another topic?
Type: quiz [any topic you want]
Example: quiz Machine Learning, quiz History, quiz Biology, etc."""
