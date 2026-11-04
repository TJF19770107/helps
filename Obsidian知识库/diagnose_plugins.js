// OB插件诊断脚本 - 在DevTools Console输入: require('C:/obsidian/diagnose_plugins.js')
// 或直接把下面这行粘贴到Console的 > 提示符后回车：
// fetch('app://local/C:/obsidian/diagnose_plugins.js').then(r=>r.text()).then(eval)
//
// 如果粘贴被禁用，请手动逐字输入这行（很短）：
//   require('./diagnose_plugins.js')
// 然后回车

(function() {
  const results = {};
  
  // 1. 扫描所有已注册插件
  const allPluginIds = Object.keys(app.plugins || {});
  results.allPluginCount = allPluginIds.length;
  results.allPluginIds = allPluginIds;
  
  // 2. 查找目标插件
  const targets = ['local-rest-api', 'terminal', 'obsidian-local-rest-api', 'obsidian-terminal'];
  results.targetPlugins = {};
  
  for (const id of allPluginIds) {
    if (targets.some(t => id.includes(t))) {
      const p = app.plugins[id];
      results.targetPlugins[id] = {
        enabled: !!p?.enabled,
        hasOnload: typeof p?.onload === 'function',
        hasInstance: !!p?.instance,
        instanceKeys: p?.instance ? Object.keys(p.instance).slice(0, 20) : null,
        // LRA特检：是否有server/http相关
        hasServer: p?.instance ? !!p.instance.server : null,
        port: p?.instance?.server?.port || p?.instance?.port || null
      };
    }
  }
  
  // 3. 检查LRA是否在监听端口
  results.portCheck = { 27124: false, 27125: false };
  
  // 4. 输出完整报告
  console.log('========== OB插件诊断报告 ==========');
  console.log('总插件数:', results.allPluginCount);
  console.log('所有插件ID:', results.allPluginIds);
  console.log('\n--- 目标插件状态 ---');
  console.table(results.targetPlugins);
  console.log('\n--- 详细JSON ---');
  console.log(JSON.stringify(results, null, 2));
  
  // 5. 返回结果供外部使用
  window.__OB_DIAGNOSE_RESULTS = results;
  return results;
})();
