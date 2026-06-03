# -*- coding: utf-8 -*-
with open('E:/myresume/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

section4 = '''
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-1: 全链路评价和质检体系如何搭建？<span class="diff d3">⭐⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p>全链路分三段评价：<b>意图识别→RAG召回→生成质量</b>，每段有独立的指标和评测方式。</p><p><b>意图识别层：</b>用人工标注的测试集（2000条，覆盖12种意图）定期跑分类准确率，监控点设在CI/CD流水线中每次模型/Prompt更新时自动触发。指标：意图准确率（目标≥90%）、实体抽取F1（目标≥85%）。</p><p><b>RAG召回层：</b>离线评测用标注的Query-Chunk正负样本对算Hit Rate@5和MRR。线上监控用间接信号——如果LLM回复中引用了知识库内容但客户继续追问（"还有吗""再说详细点"），说明召回可能不完整。</p><p><b>生成质量层：</b>三层评估——① 自动指标（BLEU/ROUGE做快速排雷，检测明显异常）；② LLM-as-a-Judge（用专门的评估模型对回复的准确性/完整性/合规性打分，每月跑一次全量）；③ 人工盲评（3名评估员各评50个case，Cohen\'s Kappa≥0.6确保一致性）。</p></div></div>
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-2: 评测用什么模型？输入数据是什么？<span class="diff d3">⭐⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p>评测模型用的是<b>GPT-4或豆包pro</b>（两者做交叉验证，结果不一致时取较低分），而不是我们自己的微调模型。原因是要避免评测偏差——用自己的模型评测自己会产生"自我感觉良好"的假象。</p><p>输入数据分三部分：<b>① 原始Query</b>（客户说的话）；<b>② Agent的完整回复</b>（待评测的对象）；<b>③ 评测上下文</b>（包括检索到的知识库chunk、调用的Tool返回结果、意图分类结果）。评测模型不是只看回复本身，而是对比"回复"和"检索结果"的一致性来判断是否存在幻觉。</p><p>给评测模型的Prompt包含评分标准和示例，要求输出结构化JSON：{faithfulness_score: 0-5, completeness_score: 0-5, issues: ["问题描述", ...], verdict: "pass"|"review"|"fail"}。</p></div></div>
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-3: 从系统日志筛选异常case，谁先判定？<span class="diff d2">⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p><b>机器先筛，人工确认。</b>三个自动触发信号：① 客户满意度评分&lt;3分（IVR调查）；② 对话轮数&gt;10轮（说明模型没理解或没解决）；③ 客户主动说"转人工""找你们领导"。这三个信号的日志会自动打上badcase标签进入待审查队列。</p><p>人工确认的流程：运营同事每天花30分钟审这批badcase（约50-80条），用LLM预分类打上初步标签（意图缺失/RAG不准/幻觉/流程bug/其他），运营只需要确认或修正。预分类准确率约80%，能省掉大部分重复劳动。</p><p>确认后的badcase进入不同的优化队列：意图缺失→补充训练数据；RAG不准→更新知识库或调整切片策略；幻觉→优化Prompt约束+补充负样本到评测集。每个优化动作完成后走回归测试→5%灰度→全量上线。</p></div></div>
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-4: 评测大模型是否挂载知识库？知识库存什么？<span class="diff d2">⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p>评测大模型<b>不挂载知识库</b>。评测的输入中已经包含了Agent检索到的知识库chunk，评测模型只需要对比"Agent回复"和"给定的知识库chunk"的一致性，不需要自己去知识库搜索。如果评测模型也挂知识库，它可能用自己的检索结果覆盖Agent的检索结果，导致评测失准——Agent实际没用到某条知识但评测模型自己查到了，误判Agent回复正确。</p><p>但评测模型挂载了<b>历史badcase库</b>作为few-shot示例。Prompt里会带3-5条历史badcase（"之前出现过的情况：客户问X，Agent回了Y，但正确的应该是Z"），让评测模型知道"什么样的回复算badcase"。这个badcase库每月更新，从已确认的badcase中采样。</p></div></div>
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-5: 评测环节打分标准是什么？<span class="diff d3">⭐⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p>三个维度各0-5分：</p><p><b>准确率（Faithfulness）</b>——回复中的每一条事实是否能从检索结果或Tool返回数据中找到对应来源。无中生有的事实扣分，引用正确的加分。阈值：4分以下标记为"review"。</p><p><b>完整性（Completeness）</b>——回复是否覆盖了客户Query中的所有需求点。客户同时问了价格和时效，回复只说了价格没提时效，扣分。阈值：3分以下标记为"fail"。</p><p><b>规范性（Compliance）</b>——回复是否符合业务规范。比如价格报价必须包含"有效期"提示、推荐方案必须包含"是否包含税费"说明、不允许使用"一定""肯定"等绝对化表述。规则来源于业务SOP，用Drools规则引擎做硬约束+LLM做软检查。</p><p>最终判定规则：三个维度都≥4分 → pass；任一维度3分 → review（人工确认）；任一维度≤2分 → fail（阻断发布）。</p></div></div>
<div class="qa"><div class="qa-q" onclick="toggle(this)">四-6: 全新未知业务场景，评测模型识别不出异常case，问题如何闭环？<span class="diff d3">⭐⭐⭐</span><span class="arrow">▶</span></div><div class="qa-a"><p>这是最棘手的情况——评测模型没见过的新场景，它不知道什么是"对"什么是"错"。我们的解法是<b>多层兜底+快速反馈闭环</b>：</p><p><b>第一层，规则兜底。</b>即使评测模型判断不出异常，业务层面的硬规则（Drools）仍然在运行。比如报价超过历史价格区间的200%、推荐了禁运品类、回复中漏掉了必填字段（如"是否含税"），规则引擎会拦截并标记需人工复核。</p><p><b>第二层，线上指标监控。</b>新场景上线后24小时内重点监控业务指标——转人工率、客户满意度、对话轮数。如果转人工率突然从12%飙到30%，说明新场景的Agent处理有问题，自动触发降级（切回人工兜底）。这不是评测模型发现的问题，是业务指标发现的。</p><p><b>第三层，快速反馈闭环。</b>一旦通过上述任意渠道发现问题，新场景的case进入badcase队列，运营24小时内完成标注，评测集3天内补充该场景的测试case。这个case加入后，下一次评测模型就能识别同类问题了。核心是<b>闭环速度</b>——从发现到补充到评测集不超过72小时。</p><p>至于"评测模型自身识别不出"的问题，我们的经验是定期（每月）用线上样本刷新评测集，用真实badcase替代老case，保证评测模型见过的场景覆盖度不低于80%。如果覆盖度低于80%，优先补充新场景的标注case。</p></div></div>
'''

# Find the agent-shop section closing
sec_idx = html.find('id="tab-agent-shop"')
close_idx = html.find('</section>', sec_idx)
if close_idx > 0:
    html = html[:close_idx] + section4 + html[close_idx:]
    with open('E:/myresume/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK - section 4 added')
else:
    print('NOT FOUND')
