# Setup Automático da Database

## ✅ O que foi implementado

Criado um **entrypoint automático** que:
1. ✅ Espera a database PostgreSQL estar pronta
2. ✅ Executa migrations automaticamente
3. ✅ Importa filmes do TMDB se a database estiver vazia
4. ✅ Inicia o servidor Django

## 📁 Arquivos Criados/Modificados

- `filmhub-backend/entrypoint.sh` - Script de inicialização
- `filmhub-backend/Dockerfile` - Atualizado para usar o entrypoint

## 🚀 Como Funciona

Quando você roda `docker-compose up`, o backend agora:

1. **Aguarda a database** estar disponível (healthcheck)
2. **Executa migrations** automaticamente (`python manage.py migrate`)
3. **Verifica se há filmes** na database
4. **Se não houver filmes**, importa automaticamente 3 páginas do TMDB (~60 filmes)
5. **Se já houver filmes**, pula a importação
6. **Inicia o servidor** Django

## 📊 Resultado

**SIM**, agora quando você roda o Docker:
- ✅ A database **vem populada** automaticamente
- ✅ O catálogo **já tem filmes** quando você acessa
- ✅ Não precisa executar comandos manuais

## 🔄 Comportamento

- **Primeira vez**: Importa ~60 filmes automaticamente
- **Próximas vezes**: Usa os filmes já existentes (não importa novamente)
- **Para reimportar**: Execute manualmente:
  ```bash
  docker-compose exec backend python manage.py import_tmdb_movies --pages 3 --clear
  ```

## ⚙️ Configuração

O script importa **3 páginas** por padrão (~60 filmes). Para mudar, edite `entrypoint.sh`:
```bash
python manage.py import_tmdb_movies --pages 5  # Importa mais filmes
```

## 🧪 Testar

1. Pare os containers: `docker-compose down`
2. Remova o volume (se quiser testar do zero): `docker-compose down -v`
3. Inicie: `docker-compose up --build`
4. Aguarde alguns segundos para a importação
5. Acesse: `http://localhost:5173` - o catálogo já terá filmes! 🎬

