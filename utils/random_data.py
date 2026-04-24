import random

def generate_us_phone():
    """
    随机生成一个符合美国格式的 10 位手机号。
    美国手机号规则简述：
    - 前 3 位是区号（NPA），不能以 0 或 1 开头，且通常第二位不能是 9
    - 中间 3 位是交换码（NXX），不能以 0 或 1 开头，且不能以 11 结尾
    - 最后 4 位是用户号码，0000 到 9999
    -ddddd
    这里为了简单起见，我们生成一个常见且看起来合理的区号和交换码组合，
    比如区号在 200-999 之间，交换码在 200-999 之间。
    """
    
    # 1. 生成 3 位区号 (Area Code): 不能以 0 或 1 开头
    area_code = random.randint(200, 999)
    
    # 2. 生成 3 位交换码 (Exchange Code): 不能以 0 或 1 开头
    exchange_code = random.randint(200, 999)
    
    # 3. 生成 4 位用户号码 (Subscriber Number): 0000 - 9999
    subscriber_number = random.randint(0, 9999)
    
    # 拼接成 10 位数字字符串 (例如：2125551234)
    # 注意：subscriber_number 需要补齐前导 0
    phone = f"{area_code}{exchange_code}{subscriber_number:04d}"
    
    return phone

if __name__ == '__main__':
    # 测试一下生成效果
    print(f"生成的随机美国手机号: {generate_us_phone()}")


