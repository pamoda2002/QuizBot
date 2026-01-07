# AI-Generated Topics Feature

## Overview
The "Most Requested Topics" feature now uses **Groq AI** to analyze actual user chat history and dynamically generate trending topics based on real user demand.

## How It Works

### 1. Data Collection
- The system collects the last **100 chat titles** across all users
- Chat titles are sorted by creation date (most recent first)
- Data is aggregated to identify patterns and trends

### 2. AI Analysis
When `/api/v1/chats/topics` is called:
1. Backend fetches recent user chat history from the database
2. Formats chat titles into a structured list
3. Sends data to **Groq AI (llama-3.3-70b-versatile model)**
4. AI analyzes patterns, frequencies, and merges similar topics
5. Returns 5-8 professionally formatted topic names

### 3. Dynamic Updates
- ✅ **Changes over time** - Topics update based on current user behavior
- ✅ **Reflects actual demand** - Based on what users are actually creating
- ✅ **Intelligent merging** - Similar topics are consolidated (e.g., "Python basics" + "Python tutorial" → "Python Programming")

## Implementation Details

### Backend Components

#### Route: `chat_routes.py`
```python
@router.get("/topics")
async def get_suggested_topics():
    # Collects last 100 chat titles across all users
    # Passes to ChatbotService for AI analysis
    # Returns AI-generated topics
```

#### Service: `chatbot_service.py`
```python
async def get_suggested_topics(user_chat_history):
    # Uses Groq AI to analyze chat patterns
    # Generates 5-8 trending topics
    # Returns JSON array of topic names
```

### AI Prompt Structure
The system sends user chat data to Groq with these instructions:
- Analyze actual user demand and frequency
- Merge similar topics into clear categories
- Keep names short and professional
- Return only JSON array (no numbering, emojis, or explanations)

### Example AI Analysis

**Input (User Chat History):**
```
- Python list comprehension tutorial
- Data Science interview prep
- Python pandas dataframe
- Machine Learning algorithms
- SQL query optimization
- Data analysis with Python
- Power BI dashboard creation
```

**Output (AI-Generated Topics):**
```json
[
  "Python Programming",
  "Data Science Interview Questions",
  "Machine Learning Algorithms",
  "SQL Query Optimization",
  "Power BI Dashboards",
  "Data Analysis",
  "Pandas DataFrames"
]
```

## Fallback Mechanism

If AI generation fails (no API key, network error, invalid response):
- System returns **fallback topics**: 
  - "Python Programming"
  - "Data Science"
  - "Web Development"
  - "Cloud Computing"
  - "React"
  - "Databases"

## Key Features

✅ **Real User Data** - Analyzes actual chat titles from your database  
✅ **AI-Powered** - Uses Groq's LLM for intelligent pattern recognition  
✅ **Dynamic Updates** - Changes as user behavior evolves  
✅ **Smart Merging** - Consolidates similar topics automatically  
✅ **Professional Format** - Clean, short topic names  
✅ **Error Handling** - Graceful fallback if AI unavailable  

## Frontend Integration

The frontend already calls this endpoint via:
```typescript
// frontend/src/services/api.ts
async getSuggestedTopics(): Promise<string[]> {
  const response = await this.api.get<{ topics: string[] }>('/chats/topics');
  return response.data.topics;
}
```

No frontend changes needed - it automatically receives the AI-generated topics!

## Testing

To test the feature:

1. **Create diverse chat sessions** with different topics
2. **Call the API endpoint**: `GET /api/v1/chats/topics`
3. **Verify response** contains 5-8 relevant topics
4. **Create more chats** and call endpoint again to see how topics adapt

Example test:
```bash
# After creating chats about Python, SQL, and React
curl http://localhost:8000/api/v1/chats/topics

# Response:
{
  "topics": [
    "Python Programming",
    "SQL Databases",
    "React Development",
    "JavaScript Fundamentals",
    "Web Development"
  ]
}
```

## Performance

- **Analysis Limit**: Last 100 chats (prevents overloading AI)
- **Response Time**: ~2-3 seconds (AI processing)
- **Caching**: Consider adding cache (e.g., update every hour)
- **API Cost**: Minimal (1 API call per topics request)

## Future Enhancements

1. **Caching** - Cache topics for 1 hour to reduce API calls
2. **Per-User Topics** - Generate personalized topics based on individual user history
3. **Trending Score** - Show which topics are gaining popularity
4. **Time-Based Analysis** - Weight recent chats higher than older ones
5. **Multi-Language** - Support topic generation in different languages
