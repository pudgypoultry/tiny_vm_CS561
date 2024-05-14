class ASTBuilder(Transformer):
	def formal(self, e):
		log.debug("-> formal")
		var_name, var_type = e
		return ast.FormalNode(var_name, var_type)

	def expr(self, e):
		log.debug("-> expr")
		return e[0]

	def plus(self, e):
		log.debug("-> plus")
		left, right = e
		return ast.MethodCallNode("plus", left, [ right ])