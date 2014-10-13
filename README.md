# fa2s

Get XML or JSON feeds to a Joomla article

- What is fa2s ?
  fa2s (Feed aggregator to static) will grab the latest data form 
  feed providers and deliver its output to a Joomla article (or
  a file).

- Why should I use it ?
  If you need an article on Joomla with the latest news from 
  some provider. 

- What do I need ?
  Python 2.7, MySQLdb and py.test


- Where are the tests?
  Tests are in the tests/ folder.  To run the tests use the
  py.test` testing tool.  

#### Docs

This script should be called from another python script. A simple example:                                                                      
```
import fa2s
import sys
logging = fa2s.getLogger()
logging.info('[START]')
api_bio_med_central = fa2s.APIBioMedCentral(3)
api_europe_pmc = fa2s.APIEuropePMC(3)
output_file = fa2s.OutputFile('result.html')
output_joomla = fa2s.OutputJoomla('server','user','password','database_name', id_article)
 # OR aggregator = fa2s.DataAggregator([api_bio_med_central,api_europe_pmc], output_file)
aggregator = fa2s.DataAggregator([api_bio_med_central,api_europe_pmc], output_joomla)
aggregator.run()
logging.info('[END]')
```

If you need any help send me an email: josemrsantos at the g00gle email 
