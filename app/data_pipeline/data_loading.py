import json

import pandas as pd


class DataLoader:
    """Classe para carregar dados de candidatos, vagas e prospecção a partir de arquivos JSON."""

    def __init__(self, base_path: str):
        """
        Inicializa a classe com o caminho base onde estão os arquivos JSON.

        :param base_path: Caminho do diretório contendo os arquivos JSON.
        """
        self.base_path = base_path

    def load_applicants(self, file_name: str) -> pd.DataFrame:
        """
        Carrega candidatos a partir de um arquivo JSON e converte para um DataFrame do pandas.

        :param file_name: Nome do arquivo JSON dentro do diretório base.
        :return: DataFrame com os dados dos candidatos.
        """
        file_path = f"{self.base_path}/{file_name}"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            applicants_list = []

            for appl_id, applicant in data.items():
                linha = {"id_applicants": appl_id}

                # Variáveis dentro da chave infos_basicas
                infos_basicas = applicant.get("infos_basicas", {})
                linha.update({
                    "telefone_recado": infos_basicas.get("telefone_recado", ""),
                    "telefone": infos_basicas.get("telefone", ""),
                    "infos_basicas_objetivo_profissional": infos_basicas.get("objetivo_profissional", ""),
                    "infos_basicas_data_criacao": infos_basicas.get("data_criacao", ""),
                    "infos_basicas_inserido_por": infos_basicas.get("inserido_por", ""),
                    "infos_basicas_email": infos_basicas.get("email", ""),
                    "infos_basicas_local": infos_basicas.get("local", ""),
                    "infos_basicas_sabendo_de_nos_por": infos_basicas.get("sabendo_de_nos_por", ""),
                    "infos_basicas_data_atualizacao": infos_basicas.get("data_atualizacao", ""),
                    "infos_basicas_codigo_profissional": infos_basicas.get("codigo_profissional", ""),
                    "infos_basicas_nome": infos_basicas.get("nome", "")
                })

                # Variáveis dentro da chave informacoes_pessoais
                pessoais = applicant.get("informacoes_pessoais", {})
                linha.update({
                    "data_aceite": pessoais.get("data_aceite", ""),
                    "nome": pessoais.get("nome", ""),
                    "cpf": pessoais.get("cpf", ""),
                    "fonte_indicacao": pessoais.get("fonte_indicacao", ""),
                    "email": pessoais.get("email", ""),
                    "email_secundario": pessoais.get("email_secundario", ""),
                    "data_nascimento": pessoais.get("data_nascimento", ""),
                    "telefone_celular": pessoais.get("telefone_celular", ""),
                    "telefone_recado": pessoais.get("telefone_recado", ""),
                    "sexo": pessoais.get("sexo", ""),
                    "estado_civil": pessoais.get("estado_civil", ""),
                    "pcd": pessoais.get("pcd", ""),
                    "endereco": pessoais.get("endereco", ""),
                    "skype": pessoais.get("skype", ""),
                    "url_linkedin": pessoais.get("url_linkedin", ""),
                    "facebook": pessoais.get("facebook", "")
                })

                # Variáveis dentro da chave informacoes_profissionais
                profissionais = applicant.get("informacoes_profissionais", {})
                linha.update({
                    "titulo_profissional": profissionais.get("titulo_profissional", ""),
                    "area_atuacao": profissionais.get("area_atuacao", ""),
                    "conhecimentos_tecnicos": profissionais.get("conhecimentos_tecnicos", ""),
                    "certificacoes": profissionais.get("certificacoes", ""),
                    "outras_certificacoes": profissionais.get("outras_certificacoes", ""),
                    "remuneracao": profissionais.get("remuneracao", ""),
                    "nivel_profissional": profissionais.get("nivel_profissional", "")
                })

                # Variáveis dentro da chave formacao_e_idiomas
                formacao = applicant.get("formacao_e_idiomas", {})
                linha.update({
                    "nivel_academico": formacao.get("nivel_academico", ""),
                    "nivel_ingles": formacao.get("nivel_ingles", ""),
                    "nivel_espanhol": formacao.get("nivel_espanhol", ""),
                    "outro_idioma": formacao.get("outro_idioma", ""),
                    "instituicao_ensino_superior": formacao.get("instituicao_ensino_superior", ""),
                    "cursos": formacao.get("cursos", ""),
                    "ano_conclusao": formacao.get("ano_conclusao", ""),
                    "download_cv": formacao.get("download_cv", ""),
                    "qualificacoes": formacao.get("qualificacoes", ""),
                    "experiencias": formacao.get("experiencias", ""),
                    "outro_curso": formacao.get("outro_curso", "")
                })

                # Variáveis dentro da chave cargo_atual
                cargo = applicant.get("cargo_atual", {})
                linha.update({
                    "id_ibrati": cargo.get("id_ibrati", ""),
                    "email_corporativo": cargo.get("email_corporativo", ""),
                    "cargo_atual": cargo.get("cargo_atual", ""),
                    "projeto_atual": cargo.get("projeto_atual", ""),
                    "cliente": cargo.get("cliente", ""),
                    "unidade": cargo.get("unidade", ""),
                    "data_admissao": cargo.get("data_admissao", ""),
                    "data_ultima_promocao": cargo.get("data_ultima_promocao", ""),
                    "nome_superior_imediato": cargo.get("nome_superior_imediato", ""),
                    "email_superior_imediato": cargo.get("email_superior_imediato", "")
                })

                # Variáveis dentro da chave cv
                linha["cv_pt"] = applicant.get("cv_pt", "")
                linha["cv_en"] = applicant.get("cv_en", "")

                applicants_list.append(linha)

            return pd.DataFrame(applicants_list)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar candidatos: {e}")
            return pd.DataFrame()

    def load_vagas(self, file_name: str) -> pd.DataFrame:
        """
        Carrega vagas a partir de um arquivo JSON e converte para um DataFrame do pandas.

        :param file_name: Nome do arquivo JSON dentro do diretório base.
        :return: DataFrame com os dados das vagas.
        """
        file_path = f"{self.base_path}/{file_name}"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            vagas_list = []

            for vaga_id, vaga in data.items():
                linha = {"id_vaga": vaga_id}

                # Variáveis dentro da chave informacoes_basicas
                info_basicas = vaga.get("informacoes_basicas", {})
                linha.update({
                    "data_requicisao": info_basicas.get("data_requicisao", ""),
                    "limite_esperado_para_contratacao": info_basicas.get("limite_esperado_para_contratacao", ""),
                    "titulo_vaga": info_basicas.get("titulo_vaga", ""),
                    "vaga_sap": info_basicas.get("vaga_sap", ""),
                    "cliente": info_basicas.get("cliente", ""),
                    "solicitante_cliente": info_basicas.get("solicitante_cliente", ""),
                    "empresa_divisao": info_basicas.get("empresa_divisao", ""),
                    "requisitante": info_basicas.get("requisitante", ""),
                    "analista_responsavel": info_basicas.get("analista_responsavel", ""),
                    "tipo_contratacao": info_basicas.get("tipo_contratacao", ""),
                    "prazo_contratacao": info_basicas.get("prazo_contratacao", ""),
                    "objetivo_vaga": info_basicas.get("objetivo_vaga", ""),
                    "prioridade_vaga": info_basicas.get("prioridade_vaga", ""),
                    "origem_vaga": info_basicas.get("origem_vaga", ""),
                    "superior_imediato": info_basicas.get("superior_imediato", "")
                })

                # Variáveis dentro da chave perfil_vaga
                perfil = vaga.get("perfil_vaga", {})
                linha.update({
                    "nome": perfil.get("nome", ""),
                    "telefone": perfil.get("telefone", ""),
                    "pais": perfil.get("pais", ""),
                    "estado": perfil.get("estado", ""),
                    "cidade": perfil.get("cidade", ""),
                    "bairro": perfil.get("bairro", ""),
                    "regiao": perfil.get("regiao", ""),
                    "local_trabalho": perfil.get("local_trabalho", ""),
                    "vaga_especifica_para_pcd": perfil.get("vaga_especifica_para_pcd", ""),
                    "faixa_etaria": perfil.get("faixa_etaria", ""),
                    "horario_trabalho": perfil.get("horario_trabalho", ""),
                    "nivel profissional": perfil.get("nivel profissional", ""),
                    "nivel_academico": perfil.get("nivel_academico", ""),
                    "nivel_ingles": perfil.get("nivel_ingles", ""),
                    "nivel_espanhol": perfil.get("nivel_espanhol", ""),
                    "outro_idioma": perfil.get("outro_idioma", ""),
                    "areas_atuacao": perfil.get("areas_atuacao", ""),
                    "principais_atividades": perfil.get("principais_atividades", ""),
                    "competencia_tecnicas_e_comportamentais": perfil.get("competencia_tecnicas_e_comportamentais", ""),
                    "demais_observacoes": perfil.get("demais_observacoes", ""),
                    "viagens_requeridas": perfil.get("viagens_requeridas", ""),
                    "equipamentos_necessarios": perfil.get("equipamentos_necessarios", "")
                })

                # Variáveis dentro da chave beneficios
                beneficios = vaga.get("beneficios", {})
                linha.update({
                    "valor_venda": beneficios.get("valor_venda", ""),
                    "valor_compra_1": beneficios.get("valor_compra_1", ""),
                    "valor_compra_2": beneficios.get("valor_compra_2", ""),
                    "data_inicial": beneficios.get("data_inicial", ""),
                    "data_final": beneficios.get("data_final", ""),
                    "habilidades_comportamentais_necessarias": beneficios.get("habilidades_comportamentais_necessarias", ""),
                    "nome_substituto": beneficios.get("nome_substituto", "")
                })

                vagas_list.append(linha)

            return pd.DataFrame(vagas_list)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar vagas: {e}")
            return pd.DataFrame()

    def load_prospects(self, file_name: str) -> pd.DataFrame:
        """
        Carrega prospecções a partir de um arquivo JSON e converte para um DataFrame do pandas.

        :param file_name: Nome do arquivo JSON dentro do diretório base.
        :return: DataFrame com os dados das prospecções.
        """
        file_path = f"{self.base_path}/{file_name}"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            prospects_list = []

            for vaga_id, vaga in data.items():
                titulo = vaga.get("titulo", "")
                modalidade = vaga.get("modalidade", "")
                prospects = vaga.get("prospects", [])

                for prospect in prospects:
                    linha = {
                        "vaga_id": vaga_id,
                        "titulo": titulo,
                        "modalidade": modalidade,
                        "quantidade_prospects": len(prospects),
                        "nome": prospect.get("nome", ""),
                        "codigo": prospect.get("codigo", ""),
                        "situacao_candidado": prospect.get("situacao_candidado", ""),
                        "data_candidatura": prospect.get("data_candidatura", ""),
                        "ultima_atualizacao": prospect.get("ultima_atualizacao", ""),
                        "comentario": prospect.get("comentario", ""),
                        "recrutador": prospect.get("recrutador", "")
                    }
                    prospects_list.append(linha)

            return pd.DataFrame(prospects_list)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar prospects: {e}")
            return pd.DataFrame()