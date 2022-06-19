import uvicorn

if __name__ == '__main__':
    uvicorn.run('root.routes:app', host='localhost', port=8000, reload=True)
