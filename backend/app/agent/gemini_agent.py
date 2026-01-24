import os
import google.generativeai as genai
from dotenv import load_dotenv

# Import your custom tools
from tools.math_solver import MathTool
from tools.search_tool import SearchTool

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

class PhysicsAgent:
    def __init__(self):
        print("🧠 Initializing Physics Agent...")
        self.math_tool = MathTool()
        self.search_tool = SearchTool()
        
        # 1. Define Tools for Gemini
        self.tools_map = {
            "solve_equation": self.math_tool.solve,
            "search_knowledge_base": self.search_tool.search
        }

        # 2. Configure Model with Tools
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', # Fast and capable
            tools=[self.math_tool.solve, self.search_tool.search],
            system_instruction="""
            You are an advanced Physics Research Assistant.
            
            Your goal is to answer complex scientific questions by:
            1. SEARCHING the vector database for context first.
            2. Identifying mathematical formulas in the text.
            3. SOLVING those formulas using the math tool if a calculation is needed.
            
            Always cite your sources from the search results (e.g., [Result 1]).
            If you calculate something, show the equation you used.
            """
        )
        
        # 3. Start Chat Session with automatic function calling enabled
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def ask(self, question: str):
        """
        Main entry point for the user.
        """
        try:
            # Send message to Gemini; it will call tools automatically if needed
            response = self.chat.send_message(question)
            return response.text
        except Exception as e:
            return f"❌ Agent Error: {str(e)}"

if __name__ == "__main__":
    # Quick Test
    agent = PhysicsAgent()
    
    print("\n--- TEST 1: General Knowledge (Should Search) ---")
    print(agent.ask("What is the limiting absorption principle mentioned in the paper?"))
    
    print("\n--- TEST 2: Math (Should Solve) ---")
    print(agent.ask("Solve the equation x^2 - 400 = 0"))