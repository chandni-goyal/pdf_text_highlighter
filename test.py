from pyautocad import Autocad, APoint
from pyautocad.contrib.tables import Table

doc_ac='/home/techstriker/Downloads/other_pdfs/carlino.pdf'
data = Table.data_from_file(doc_ac)

