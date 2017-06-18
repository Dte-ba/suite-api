V = \033[92m
N = \033[0m


all:
	@echo ""
	@echo "Comandos disponibles:"
	@echo ""
	@echo "   ${V}deploy${N}     Realiza el deploy sobre dokku."
	@echo ""

deploy:
	git push origin
	git push dokku master
