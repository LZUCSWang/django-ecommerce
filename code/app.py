# ...existing code...

@app.route('/comment_analysis/')
def comment_analysis():
    try:
        # 添加调试日志
        print("Processing comment_analysis request")
        # 你的数据处理代码
        data = [
            {"key": "店铺1", "value": 100},
            {"key": "店铺2", "value": 90},
            # ... 更多数据
        ]
        print("Returning data:", data)  # 添加调试日志
        return jsonify(data)
    except Exception as e:
        print("Error in comment_analysis:", str(e))  # 添加错误日志
        return jsonify({"error": str(e)}), 500

# ...existing code...
