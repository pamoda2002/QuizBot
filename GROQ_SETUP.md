# QuizBot with Groq LLM Integration

## Overview
QuizBot now uses **Groq's LLM (Llama 3.3 70B)** with LPU-based acceleration for intelligent, dynamic conversational responses instead of rule-based answers.

## What Changed?

### Before (Rule-Based QuizBank)
- ❌ Pre-defined questions and answers
- ❌ Limited topics
- ❌ Static responses
- ❌ No conversational context

### After (Groq LLM)
- ✅ Dynamic AI-generated responses
- ✅ Unlimited topics and knowledge
- ✅ Natural conversations
- ✅ Context-aware responses
- ✅ Ultra-fast inference with Groq LPU

## Features
- 🤖 **AI-Powered Conversations**: Natural language understanding
- ⚡ **Lightning Fast**: Groq's LPU technology for instant responses
- 📚 **Educational Assistant**: Help with learning any topic
- 💬 **Context Awareness**: Remembers conversation history
- 🎓 **Smart Tutoring**: Explains concepts, answers questions

## Setup Instructions

### 1. Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy your API key

### 2. Configure Environment

Create a `.env` file in the `backend` folder:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Install Dependencies

The `groq` package should already be installed. If not:

```bash
cd backend
pip install -r requirements.txt
```

### 4. Start the Server

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 5. Start the Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

Open http://localhost:3000

## Usage Examples

### General Conversations
```
User: Hello!
Bot: Hello! 👋 I'm QuizBot, your friendly AI assistant. How can I help you today?

User: Tell me about Python
Bot: Python is a high-level, interpreted programming language...
```

### Learning & Education
```
User: Can you quiz me on JavaScript?
Bot: Of course! Let's test your JavaScript knowledge. Here's a question...

User: Explain how functions work
Bot: Great question! Functions are reusable blocks of code...
```

### Any Topic
```
User: What is photosynthesis?
Bot: Photosynthesis is the process by which plants...

User: Help me understand calculus
Bot: I'd be happy to help! Calculus is the study of...
```

## How It Works

### 1. **User Sends Message**
- Frontend sends message to backend API
- Message includes conversation history

### 2. **Context Building**
- Last 10 messages are used for context
- System prompt defines QuizBot's personality
- Current message is added

### 3. **Groq LLM Processing**
- Model: `llama-3.3-70b-versatile`
- Ultra-fast inference with LPU acceleration
- Temperature: 0.7 (balanced creativity)
- Max tokens: 1024

### 4. **Response Delivery**
- AI-generated response sent back
- Displayed in chat interface
- Conversation history updated

## Technical Details

### Model Configuration
```python
model="llama-3.3-70b-versatile"  # Groq's fastest, most capable model
temperature=0.7                   # Balanced between creative and focused
max_tokens=1024                   # Sufficient for detailed responses
top_p=1                          # Full probability distribution
```

### System Prompt
QuizBot is configured as:
- Friendly and helpful AI assistant
- Educational focus
- Concise but informative
- Emoji usage for engagement
- Multi-topic expertise

### Context Window
- Maintains last 10 messages for context
- Prevents token limit issues
- Preserves conversation flow

## API Endpoint

### Send Message
```http
POST /api/v1/messages/send
Content-Type: application/json

{
  "chat_id": "chat123",
  "content": "Your message here"
}
```

**Response:**
```json
{
  "user_message": {
    "id": "msg1",
    "role": "user",
    "content": "Your message here",
    ...
  },
  "bot_message": {
    "id": "msg2",
    "role": "assistant",
    "content": "AI-generated response",
    ...
  }
}
```

## Groq LPU Technology

### What is LPU?
- **Language Processing Unit**: Custom silicon designed for LLM inference
- **10x Faster**: Than traditional GPU inference
- **Lower Latency**: Real-time conversational experiences
- **Cost Effective**: Free tier available

### Performance
- **Response Time**: ~0.5-2 seconds
- **Throughput**: 300+ tokens/second
- **Model Size**: 70B parameters
- **Quality**: State-of-the-art responses

## Troubleshooting

### "AI service is not configured"
**Problem**: Groq API key not set

**Solution**:
1. Check `.env` file exists in `backend/`
2. Verify `GROQ_API_KEY` is set correctly
3. Restart the backend server

### "ModuleNotFoundError: No module named 'groq'"
**Problem**: Groq package not installed

**Solution**:
```bash
cd backend
pip install groq
```

### Slow Responses
**Problem**: Network or API issues

**Solution**:
1. Check internet connection
2. Verify Groq API status: https://status.groq.com/
3. Check API rate limits on Groq console

### Empty or Error Responses
**Problem**: API quota exceeded or invalid key

**Solution**:
1. Check Groq console for usage limits
2. Verify API key is valid
3. Check backend logs for error messages

## Comparison: Rule-Based vs LLM

| Feature | QuizBank (Before) | Groq LLM (After) |
|---------|------------------|------------------|
| Response Type | Static templates | AI-generated |
| Topics | 6 predefined | Unlimited |
| Flexibility | Low | High |
| Conversation | No | Yes |
| Context Awareness | No | Yes |
| Learning | Fixed questions | Adaptive |
| Speed | Instant | ~1-2 seconds |
| Knowledge | Limited | Vast |

## Best Practices

### For Users
- ✅ Ask clear, specific questions
- ✅ Provide context when needed
- ✅ Use natural language
- ✅ Follow up for clarification

### For Developers
- ✅ Monitor API usage
- ✅ Handle errors gracefully
- ✅ Keep conversation history manageable
- ✅ Use appropriate temperature settings
- ✅ Set reasonable token limits

## Cost & Limits

### Groq Free Tier
- **Requests**: Generous free tier
- **Rate Limits**: Check Groq console for current limits
- **Models**: Full access to Llama models

### Paid Plans
- Available for higher usage
- Enterprise options available
- Check https://groq.com/pricing

## Security

- ✅ API key stored in environment variables
- ✅ Never commit `.env` to version control
- ✅ Use `.env.example` for templates
- ✅ Validate user input
- ✅ Rate limiting on backend

## Future Enhancements

Potential improvements:
- [ ] Streaming responses for real-time typing effect
- [ ] Multi-turn quiz generation
- [ ] Custom system prompts per user
- [ ] Response caching
- [ ] Fine-tuned models
- [ ] Image understanding (when available)

## Support Resources

- **Groq Documentation**: https://console.groq.com/docs
- **Groq Community**: https://groq.com/community
- **API Status**: https://status.groq.com/
- **Model Info**: https://console.groq.com/docs/models

## Example Interactions

### Coding Help
```
User: How do I reverse a string in Python?
Bot: There are several ways to reverse a string in Python! Here are the most common methods:

1. **Using slicing** (most Pythonic):
   ```python
   text = "hello"
   reversed_text = text[::-1]  # "olleh"
   ```

2. **Using reversed() function**:
   ```python
   text = "hello"
   reversed_text = ''.join(reversed(text))
   ```

Would you like me to explain any of these methods in detail? 🐍
```

### Science Questions
```
User: Explain the water cycle
Bot: The water cycle is the continuous movement of water on, above, and below Earth's surface! 💧

Here's how it works:

1. **Evaporation**: Sun heats water → becomes vapor ☀️
2. **Condensation**: Vapor cools → forms clouds ☁️
3. **Precipitation**: Clouds release water as rain/snow 🌧️
4. **Collection**: Water returns to oceans/lakes 🌊

This cycle repeats endlessly, providing fresh water for life on Earth!
```

## Contributing

To improve the chatbot:
1. Adjust system prompt in `chatbot_service.py`
2. Modify temperature for different response styles
3. Add custom tools/functions for specific tasks
4. Enhance error handling

---

**Enjoy your AI-powered QuizBot! 🤖✨**
