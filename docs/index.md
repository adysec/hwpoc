---
layout: default
title: 首页
---
<div class="doc-topbar">
  <div class="doc-title">
    <a href="{{ '/' | relative_url }}">{{ site.title }}</a>
    <small>护网漏洞情报</small>
  </div>
  <div class="doc-actions">
    <button class="theme-btn" onclick="toggleTheme()" title="切换主题">🌙</button>
    <a class="btn" href="#" onclick="openModal();return false">＋ 提交漏洞</a>
    <a class="btn btn-outline" href="https://github.com/adysec/hwpoc" target="_blank">GitHub</a>
  </div>
</div>

{% assign y2026 = site.data["2026"] | size %}
{% assign y2025 = site.data["2025"] | size %}
{% assign y2024 = site.data["2024"] | size %}
{% assign y2023 = site.data["2023"] | size %}
{% assign total = y2026 | plus: y2025 | plus: y2024 | plus: y2023 %}

<div class="home-page">
  <h2>护网漏洞库</h2>
  <p>护网（HW）期间漏洞情报汇总 · 0day / 1day / nday</p>
  <div class="home-cards">
    <a class="home-card" href="{{ '/2025/' | relative_url }}">
      <span class="num">{{ y2025 }}</span>
      <span class="lbl">2025 年</span>
    </a>
    <a class="home-card" href="{{ '/2024/' | relative_url }}">
      <span class="num">{{ y2024 }}</span>
      <span class="lbl">2024 年</span>
    </a>
    <a class="home-card" href="{{ '/2023/' | relative_url }}">
      <span class="num">{{ y2023 }}</span>
      <span class="lbl">2023 年</span>
    </a>
  </div>
  <div class="home-links">
    <a class="btn" href="#" onclick="openModal();return false">＋ 提交漏洞</a>
    <a class="btn btn-outline" href="https://github.com/adysec/hwpoc">GitHub 仓库</a>
  </div>
</div>

<div class="modal-overlay" id="submitModal">
  <div class="modal-box">
    <div class="modal-header">
      <h3>提交漏洞</h3>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="form-row">
        <div class="form-group"><label>厂商 <span class="req">*</span></label><input id="f_vendor" placeholder="如 深信服、奇安信、用友"></div>
        <div class="form-group"><label>漏洞名称 <span class="req">*</span></label><input id="f_name" placeholder="如 CVE-2025-XXXX 或 产品名+类型"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>漏洞类型 <span class="req">*</span></label><input id="f_type" placeholder="如 RCE、SQL注入、未授权访问"></div>
        <div class="form-group"><label>涉及版本</label><input id="f_version" placeholder="受影响版本号或范围"></div>
      </div>
      <div class="form-group"><label>利用路径 / URL</label><input id="f_path" placeholder="漏洞触发路径或接口"></div>
      <div class="form-group"><label>漏洞详情 / POC</label><textarea id="f_detail" rows="3" placeholder="请在此粘贴 POC 或漏洞详情"></textarea></div>
      <div class="form-group"><label>处置建议 / 修复方案</label><textarea id="f_fix" rows="2" placeholder="升级版本、补丁链接、临时缓解措施"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>情报获取时间</label><input id="f_date" placeholder="如 0630、0701"></div>
        <div class="form-group"><label>来源 / 验证人</label><input id="f_source" placeholder="提交者昵称或来源"></div>
      </div>
      <div class="form-group">
        <label>标签 <span class="req">*</span></label>
        <div class="radio-group">
          <label><input type="radio" name="label" value="0day"> 0day</label>
          <label><input type="radio" name="label" value="1day"> 1day</label>
          <label><input type="radio" name="label" value="nday"> nday</label>
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" onclick="closeModal()">取消</button>
      <button class="btn" onclick="submitVuln()">提交 Issue</button>
    </div>
  </div>
</div>

<script>
function openModal() { document.getElementById('submitModal').classList.add('active'); }
function closeModal() { document.getElementById('submitModal').classList.remove('active'); }
document.getElementById('submitModal').addEventListener('click', function(e) { if (e.target === this) closeModal(); });
window.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });
function submitVuln(year) {
  var vendor = document.getElementById('f_vendor').value.trim();
  var name = document.getElementById('f_name').value.trim();
  var type = document.getElementById('f_type').value.trim();
  var version = document.getElementById('f_version').value.trim();
  var path = document.getElementById('f_path').value.trim();
  var detail = document.getElementById('f_detail').value.trim();
  var fix = document.getElementById('f_fix').value.trim();
  var date = document.getElementById('f_date').value.trim();
  var source = document.getElementById('f_source').value.trim();
  var labelEl = document.querySelector('input[name="label"]:checked');
  var label = labelEl ? labelEl.value : '';
  if (!vendor || !name || !type || !label) { alert('请填写厂商、漏洞名称、漏洞类型和标签（必填项）'); return; }
  var title = '[' + (year || '') + '] ' + name;
  var body = '### 厂商 *\n' + vendor + '\n\n### 漏洞名称 *\n' + name + '\n\n### 漏洞类型 *\n' + type + '\n\n' +
    (version ? '### 涉及版本\n' + version + '\n\n' : '') +
    (path ? '### 利用路径 / URL\n' + path + '\n\n' : '') +
    (detail ? '### 漏洞详情 / POC\n```\n' + detail + '\n```\n\n' : '') +
    (fix ? '### 处置建议 / 修复方案\n' + fix + '\n\n' : '') +
    (date ? '### 情报获取时间\n' + date + '\n\n' : '') +
    '### 标签 *\n- [x] ' + label + '\n\n' +
    (source ? '### 来源 / 验证人\n' + source + '\n\n' : '') +
    '---\n\n**提交前请确认：**\n- [ ] 该漏洞尚未存在于当前漏洞库中\n- [ ] 信息准确，POC 经过验证或注明来源\n- [ ] 已去除敏感信息（如内部 IP、密码等）';
  var url = 'https://github.com/adysec/hwpoc/issues/new?labels=漏洞提交&template=submit-vulnerability.md&title=' +
    encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  window.open(url, '_blank');
  closeModal();
}
</script>
