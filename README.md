# 🎯 Day in the Life: AI-Powered Career Simulator

An interactive career exploration tool that uses multi-agent AI to simulate realistic workday scenarios. Experience any career through intelligent agents that research, design scenarios, evaluate decisions, and narrate your journey.
## Demo: https://dayinthelife-umqggyfqqwg2qwgecqnxlo.streamlit.app/
## 🌟 Features

- **Multi-Agent AI System**: Four specialized AI agents work together:
  - 🔍 **Research Agent**: Analyzes career requirements and knowledge gaps
  - 🎨 **Scenario Designer**: Creates realistic workplace challenges
  - ⚖️ **Evaluator**: Assesses decisions and determines consequences
  - 📖 **Narrator**: Weaves everything into an engaging story

- **ReAct Pattern**: Agents use Reason-Act-Observe loop for intelligent decision-making
- **Interactive Storytelling**: Your choices shape the narrative
- **Skill Tracking**: Monitors skills demonstrated throughout the simulation
- **Real-time Processing**: See agents collaborate in real-time

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- NVIDIA NIM API key ([Get one here](https://build.nvidia.com/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Khushibhansali/DayInTheLife.git
cd DayInTheLife
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

4. Enter your NVIDIA API key in the sidebar and start exploring careers!

## 🛠️ Tech Stack

- **Python** - Core programming language
- **OpenAI SDK** - LLM client interface
- **NVIDIA NIM** - AI inference platform
- **Nemotron Nano 9B v2** - Language model
- **Streamlit** - Web interface
- **JSON** - Data serialization

## 📦 Project Structure

```
DayInTheLife/
├── streamlit_app.py      # Main application with UI + agent logic
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🎮 How It Works

1. **Enter a Career**: Choose any profession (Software Engineer, Chef, Doctor, etc.)
2. **Agent Research**: AI agents analyze what they need to know about the career
3. **Scenario Generation**: Realistic workplace situations are created
4. **Make Decisions**: Choose how to handle each situation
5. **See Consequences**: Agents evaluate your choices and advance the story
6. **Track Progress**: See which skills you've demonstrated

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add API key to Secrets (Settings → Secrets)
5. Deploy!

**Cost**: Free for public repos, $20/month for private

### Alternative Platforms
- **Heroku**: $5-7/month (Eco Dynos)
- **Vercel**: Not recommended (Python support limited)

## 🔐 Security Note

**Never commit API keys to version control!**

Use environment variables or Streamlit secrets:
```python
# In Streamlit Cloud: Settings → Secrets
NVIDIA_API_KEY = "your-key-here"

# In code:
api_key = st.secrets["NVIDIA_API_KEY"]
```

## 💡 Example Careers to Try

- Software Engineer
- Emergency Room Doctor
- Restaurant Chef
- Marketing Manager
- Flight Attendant
- Wildlife Photographer
- High School Teacher
- Cybersecurity Analyst

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [NVIDIA NIM](https://build.nvidia.com/) AI platform
- Powered by Nemotron Nano 9B v2 language model
- UI built with [Streamlit](https://streamlit.io/)

## 📧 Contact

Khushi Bhansali - [@Khushibhansali](https://github.com/Khushibhansali)

Project Link: [https://github.com/Khushibhansali/DayInTheLife](https://github.com/Khushibhansali/DayInTheLife)

---

**Made with ❤️ for career exploration and AI experimentation**
