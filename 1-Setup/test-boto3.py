def main():
    print("Hello, World!")

    try:
        import boto3
        print("boto3 is installed.")
        print("boto3 version:", boto3.__version__)
    except ImportError:
        print("boto3 is NOT installed.")

if __name__ == "__main__":
    main()

