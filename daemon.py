#!/usr/bin/env python


#mall_urls=["https://www.smzdm.com/mall/cebbank/"]
#m = MallPlugin(mall_urls)
#m.start()
#
#search_urls=["http://search.smzdm.com/?c=home&s=%E5%85%89%E5%A4%A7&order=score&mall_id=1065"]
#s = SearchPlugin(search_urls)
#s.start()

import utils
import plugins
import data

from pydoc import locate

plugins = []
for p in data.enabled_plugins:
    plugin = locate(p)
    plugins.append(plugin)

print plugins
for plugin in plugins:
    inst = plugin()
    inst.start()
