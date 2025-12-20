"""
OpenAI Service for PF Resource Hub
Handles HVAC troubleshooting chat using OpenAI's GPT API with Simple RAG
"""

import os
from openai import OpenAI
from typing import List, Dict
from simple_rag import search_docs

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI service"""
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ OpenAI initialized successfully")
        else:
            self.client = None
            print("⚠️  OPENAI_API_KEY not configured. AI chat will not work.")
    
    def get_hvac_system_prompt(self, context: str = "", sources: List[str] = None) -> str:
        """
        System prompt to make GPT an HVAC troubleshooting expert
        Now includes retrieved context from documentation
        """
        base_prompt = """You are an expert HVAC technician assistant for Planet Fitness and Save Energy Systems.

Your role:
- Answer questions using ONLY the provided documentation context
- Help troubleshoot HVAC problems with clear, step-by-step guidance
- Provide practical solutions from the official SES documentation
- Focus on Planet Fitness gym equipment and commercial HVAC systems
- Be concise but thorough - prioritize actionable advice
- Use simple language that both experienced and new technicians can understand

CRITICAL RULES:
- ONLY use information from the context provided below
- If the answer is not in the context, say: "I don't have that specific information in our documentation. Please call SES support at (617) 564-4800"
- Always cite the source document when answering
- Never make up information or guess
- If context mentions calling SES, include that number: (617) 564-4800

"""
        
        if context and sources:
            base_prompt += f"\n\n📚 OFFICIAL SES DOCUMENTATION CONTEXT:\n\n{context}\n\n"
            base_prompt += f"📄 Sources: {', '.join(sources)}\n\n"
            base_prompt += "Use ONLY the above context to answer. Cite sources in your response.\n"
        else:
            base_prompt += "\n⚠️ No relevant documentation found. Direct user to call SES: (617) 564-4800\n"
        
        return base_prompt
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Send a message to OpenAI with RAG-enhanced context
        
        Args:
            user_message: The user's question
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI response string
        """
        if not self.client:
            return "❌ AI service is not configured. Please contact your administrator."
        
        try:
            # 🔍 STEP 1: Search documentation for relevant context
            print(f"🔍 Searching docs for: {user_message}")
            context, sources = search_docs(user_message)
            print(f"📄 Found sources: {sources}")
            
            # 🤖 STEP 2: Build system prompt with retrieved context
            system_prompt = self.get_hvac_system_prompt(context, sources)
            
            # 🗨️ STEP 3: Build messages for OpenAI
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-6:]:  # Keep last 6 messages for context
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # 💭 STEP 4: Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Fast and cost-effective
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            # Add sources citation to response
            if sources:
                response_text += f"\n\n---\n📄 **Sources:** {', '.join(sources)}"
            
            return response_text
        
        except Exception as e:
            print(f"❌ OpenAI API error: {str(e)}")
            return f"I'm having trouble connecting right now. Please try again in a moment. (Error: {str(e)[:100]})"


# Module-level instance
_openai_service = OpenAIService()

def get_ai_response(user_message: str, conversation_history: List[Dict] = None) -> str:
    """
    Wrapper function to get AI response
    
    Args:
        user_message: User's question
        conversation_history: Previous messages
    
    Returns:
        AI response
    """
    return _openai_service.chat(user_message, conversation_history)


# Test the service
if __name__ == "__main__":
    print("\n🧪 Testing OpenAI Service...")
    
    # Test basic question
    response = get_ai_response("My AC unit isn't cooling. What should I check first?")
    print(f"\n💬 Test Question: My AC unit isn't cooling. What should I check first?")
    print(f"\n🤖 AI Response:\n{response}")
    
    # Test with conversation history
    history = [
        {"role": "user", "content": "My AC isn't cooling"},
        {"role": "assistant", "content": "Let's troubleshoot. First, check if the thermostat is set to COOL mode."}
    ]
    response2 = get_ai_response("It's set to cool mode, what's next?", history)
    print(f"\n💬 Follow-up: It's set to cool mode, what's next?")
    print(f"\n🤖 AI Response:\n{response2}")
    
    print("\n✅ OpenAI service test complete!")
