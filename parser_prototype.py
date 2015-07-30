import pyparser as pp

if self.prep in string:
    x = pp.SkipTo(self.prep) + self.prep + pp.Word(pp.alphas)
else:
    x = pp.Word(pp.alphas+" ")
    
blueprint_condition = pp.Word(pp.alphas).setParseAction + pp.Word(bp_keywords, max=1) +\
            pp.Word(pp.alphas)

