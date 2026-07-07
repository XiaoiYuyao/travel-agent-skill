"""
============================================
  Build with Claude 市场提交助手
============================================
  把你的 travel-agent-skill 提交到
  Build with Claude 插件市场

  作者: XiaoiYuyao
  GitHub: https://github.com/XiaoiYuyao
============================================
"""

STEPS = """
🚀 提交到 Build with Claude 插件市场 · 操作步骤

========== 前置条件 ==========
1. 注册 GitHub 账号: https://github.com (已有 ✅)
2. Fork 仓库: https://github.com/davepoon/buildwithclaude
   → 点右上角 "Fork" 按钮

========== 操作步骤 ==========

Step 1: Fork 仓库后，克隆到本地
—————————————————————
  git clone https://github.com/XiaoiYuyao/buildwithclaude.git
  cd buildwithclaude

Step 2: 创建插件目录
—————————————————————
  mkdir -p plugins/travel-agent-skill

Step 3: 复制 SKILL.md 到插件目录
—————————————————————
  copy D:\\App\\Agent\\.claude\\skills\\travel-agent-skill.md plugins\\travel-agent-skill\\SKILL.md

  (或者把完整的 scripts/ 目录也放进去)
  cp -R D:\\App\\Agent\\Skills\\travel-agent-skill\\scripts plugins\\travel-agent-skill\\

Step 4: 编辑 marketplace.json
—————————————————————
  打开 .claude-plugin/marketplace.json
  在 plugins 数组末尾添加以下内容：

===== 从下面复制 =====
{
  "name": "travel-agent-skill",
  "description": "私人旅行管家 — 输入出发地/目的地/天数/预算，一键生成完整HTML旅行攻略。包含每日交通衔接、酒店住宿、景点安排、美食推荐、打车衔接，支持一键跳转12306/携程/大众点评/高德/小红书，美食直达小红书搜索攻略。生成的文件保存到桌面，双击即可查看，无需任何服务器或登录。",
  "version": "3.1.0",
  "author": {
    "name": "XiaoiYuyao",
    "url": "https://github.com/XiaoiYuyao"
  },
  "repository": "https://github.com/XiaoiYuyao/travel-agent-skill",
  "license": "MIT",
  "keywords": ["travel","travel-agent","trip-planning","itinerary","tour-guide","travel-planner","攻略","旅行"],
  "category": "productivity",
  "source": "https://github.com/XiaoiYuyao/travel-agent-skill"
}
===== 复制到上面 =====

Step 5: 提交并推送
—————————————————————
  git add plugins/travel-agent-skill/
  git add .claude-plugin/marketplace.json
  git commit -m "✨ 新增 travel-agent-skill: 私人旅行管家插件"
  git push origin main

Step 6: 创建 Pull Request
—————————————————————
  打开浏览器访问:
  https://github.com/XiaoiYuyao/buildwithclaude

  点击 "Contribute" → "Open Pull Request"
  填写标题: "Add travel-agent-skill: AI-powered travel itinerary generator"
  填写描述:

===== PR 描述模板 =====
  ## ✈️ travel-agent-skill · 私人旅行管家

  ### 功能
  - 🚄 输入出发地/目的地/天数/预算，一键生成完整攻略
  - 🏨 每日行程含交通衔接、酒店、景点、美食、打车
  - 💰 预算透明，进度条显示
  - 🔗 一键跳转12306/携程/大众点评/高德
  - 🍜 美食直达小红书搜索攻略
  - 🖥️ 生成自包含HTML文件，双击即可查看，无需服务器
  - 📱 响应式设计，手机电脑都能看

  ### 作者
  - **XiaoiYuyao**
  - GitHub: https://github.com/XiaoiYuyao/travel-agent-skill
  - 示例: https://github.com/XiaoiYuyao/travel-agent-skill/examples/guiyang_3days_sample.html

  ### 安装方式
  ```bash
  npx skills add XiaoiYuyao/travel-agent-skill
  ```
  或在 Claude Code 中说「帮我规划旅行」

  ### 截图
  见 examples/ 目录

===== 复制到上面 =====

Step 7: 等待审核
—————————————————————
  提交后等待 davepoon 合并你的 PR
  合并后，你的 skill 就会出现在
  /plugin search @buildwithclaude 中

========== 合并后用户如何安装 ==========
/plugin marketplace add davepoon/buildwithclaude
/plugin search @buildwithclaude   (能看到你的 skill)
/plugin install travel-agent-skill@buildwithclaude

🎉 恭喜！你的第一个 Claude Code Skill 上线了！
"""

if __name__ == "__main__":
    print(STEPS)
    input("\n按回车键确认已理解上述步骤...")
    print("\n✅ 祝你的 skill 大受欢迎！")
