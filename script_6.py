import zipfile
import io

zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for file_path, content in project_files.items():
        zip_file.writestr(file_path, content)

zip_buffer.seek(0)
with open('Dynamic-AI-Chatbot-Complete.zip', 'wb') as f:
    f.write(zip_buffer.getvalue())

print("✅ Complete project created successfully!")
print("\n📦 Files included in the package:")
for file_path in sorted(project_files.keys()):
    print(f"   {file_path}")

print(f"\n🎉 Your complete Dynamic AI Chatbot project is ready!")
print(f"📁 File: Dynamic-AI-Chatbot-Complete.zip")
print(f"📏 Total files: {len(project_files)}")

file_sizes = {}
total_size = 0
for file_path, content in project_files.items():
    size = len(content.encode('utf-8'))
    file_sizes[file_path] = size
    total_size += size

print(f"📊 Total project size: {total_size:,} bytes ({total_size/1024:.1f} KB)")

print("\n📋 File sizes:")
for file_path, size in sorted(file_sizes.items()):
    print(f"   {file_path:<25} {size:>6,} bytes")

print(f"\n🚀 Ready to use! Follow these steps:")
print(f"   1. Download 'Dynamic-AI-Chatbot-Complete.zip'")
print(f"   2. Extract it to your desired folder")
print(f"   3. Open the folder in PyCharm")
print(f"   4. Install requirements: pip install -r requirements.txt")
print(f"   5. Run: python server.py")
print(f"   6. Open http://localhost:5000 in your browser")
print(f"   7. Start chatting with your AI! 🤖")