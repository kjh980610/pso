import pso
import cal_yan

pso1 = pso.pso( p_num = 30, max_iter = 30)
link = pso1.run()

cal_yan.print_link(link)