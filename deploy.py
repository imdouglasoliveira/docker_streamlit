import os
import subprocess
import fileinput
import sys
from pathlib import Path
from datetime import datetime

def run_command(command, error_message="Erro ao executar comando"):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        return False

def check_disk_space():
    """Verifica e exibe o espaço em disco disponível"""
    print("\nVerificando espaço em disco...")
    run_command("df -h /", "Erro ao verificar espaço em disco")

def clean_system():
    """Limpa containers, imagens, volumes e cache do sistema"""
    print("\nIniciando limpeza do sistema...")
    
    commands = [
        ("docker container prune -f", "Removendo containers parados..."),
        ("docker image prune -a -f", "Removendo imagens não utilizadas..."),
        ("docker volume prune -f", "Removendo volumes não utilizados..."),
        ("docker network prune -f", "Removendo networks não utilizadas..."),
        ("docker system prune -af", "Limpando sistema Docker..."),
        ("apt-get clean", "Limpando cache do apt..."),
        ("apt-get autoremove -y", "Removendo pacotes não utilizados...")
    ]
    
    for cmd, msg in commands:
        print(msg)
        run_command(cmd, f"Aviso durante: {msg}")
    
    print("Limpeza do sistema concluída!\n")

def update_production_flag(config_file, set_to_true=True):
    try:
        with fileinput.FileInput(config_file, inplace=True) as file:
            for line in file:
                if "production = " in line:
                    print(f"    production = {str(set_to_true)}")
                else:
                    print(line, end='')
        return True
    except Exception as e:
        print(f"Erro ao atualizar arquivo de configuração: {e}")
        return False

def update_version(config_file):
    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if 'version = "' in line:
                current_version = line.split('"')[1]
                parts = current_version.split('.')
                
                if len(parts) == 2:
                    new_version = f'{parts[0]}.{parts[1]}.1'
                else:
                    new_version = f'{parts[0]}.{parts[1]}.{int(parts[2]) + 1}'
                
                print(f'    version = "{new_version}"')
            else:
                print(line, end='')

def update_deploy_timestamp():
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    deploy_file = Path("last_deploy.txt")
    with open(deploy_file, 'w') as f:
        f.write(timestamp)
    print(f"Timestamp de deploy atualizado: {timestamp}")

def check_and_prepare():
    """Verifica e prepara o ambiente para o deploy"""
    print("\nPreparando ambiente para deploy...")
    check_disk_space()
    clean_system()
    print("Ambiente preparado!")

def deploy():
    try:
        # Diretório do projeto
        project_dir = "/root/.../"
        
        # Mudar para o diretório do projeto
        os.chdir(project_dir)
        print(f"\nMudando para o diretório: {project_dir}")

        # Verificar e preparar ambiente
        check_and_prepare()

        # Reset e atualização do Git
        print("\nAtualizando código do repositório...")
        if not run_command("git reset --hard origin/main", "Erro ao resetar repositório"):
            return False
        if not run_command("git pull --force origin main", "Erro ao buscar alterações do GitHub"):
            return False

        # Remover serviço existente
        print("\nRemovendo serviço anterior...")
        run_command("docker service rm nome_servico", "Aviso: Serviço não encontrado para remoção")

        # Atualizar flag de produção
        print("\nAtualizando configurações...")
        config_file = Path("config/config.py")
        if not update_production_flag(config_file):
            return False
        
        # Atualizar versão e timestamp
        update_version(config_file)
        update_deploy_timestamp()

        # Construir nova imagem
        print("\nConstruindo nova imagem Docker...")
        if not run_command("docker build --no-cache -t nome_imagem .", "Erro ao construir imagem Docker"):
            return False

        # Criar novo container
        print("\nIniciando novo serviço...")
        if not run_command("docker stack deploy -c docker-compose.yaml nome_container", "Erro ao criar container"):
            return False

        print("\n✨ Deploy concluído com sucesso! ✨")
        return True
    
    except Exception as e:
        print(f"\n❌ Erro durante o deploy: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        if deploy():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Deploy interrompido pelo usuário")
        sys.exit(1)