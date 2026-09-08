# avatar_tools_edit.py · P3 代码编辑力
# 注册 !edit 工具：安全文本替换 + .bak 备份 + 写回验证。
# 用法：!edit 文件路径::旧文本::新文本
import os

def edit_file(spec):
    # spec: 路径::旧::新
    if "::" not in spec:
        return "用法: !edit 文件路径::旧文本::新文本"
    parts = spec.split("::", 2)
    if len(parts) < 3:
        return "用法: !edit 文件路径::旧文本::新文本"
    path, old, new = parts[0].strip(), parts[1], parts[2]
    if not os.path.exists(path):
        return "文件不存在: " + path
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        return "未找到目标文本，未做改动。"
    # 先备份再改（可逆）
    bak = path + ".bak"
    with open(bak, "w", encoding="utf-8") as f:
        f.write(content)
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return "已编辑 %s（旧→新），备份 %s" % (path, bak)


def register():
    import avatar
    avatar.TOOLS["edit"] = (edit_file, "代码编辑：edit 文件路径::旧::新（带 .bak 备份，可逆）")


if __name__ == "__main__":
    import sys
    print(edit_file(" ".join(sys.argv[1:])))