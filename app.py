from website import create_app

print("Creating app...")
app = create_app()

if __name__ == '__main__':
    print("Running app...")
    app.run(debug=True)
