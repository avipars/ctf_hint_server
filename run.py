from hints import create_app

print("Running Flask Server")

app = create_app()

if __name__ == "__main__":
    # app.run(debug=True, port="5000") #debug ,

    app.run(debug=True, host="0.0.0.0", port=8080)  # production