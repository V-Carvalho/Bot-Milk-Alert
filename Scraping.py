import os
import time
import dotenv
import asyncio
from processing import Processing
from playwright.async_api import async_playwright

processing = Processing()
dotenv.load_dotenv(dotenv.find_dotenv())

while True:
    print('rodou')

    async def run(playwright):
        milk_list = []
        total_items_page = 30
        url = os.getenv('URL_CARREFOUR')

        # Criando o navegador
        browser = await playwright.chromium.launch(headless=False)
        # Criando uma nova pagina no browser
        page = await browser.new_page()
        # Abrindo url na pagina crianda
        await page.goto(url)
        await page.wait_for_timeout(5000)

        # Preenchendo o formulário da home
        try:
            await page.click('button:has-text("Receba em Casa")')
            await page.wait_for_timeout(5000)
            await page.locator('#zipcode').fill("05134-220")
            await page.wait_for_timeout(5000)
            await page.click('button:has-text("Buscar")')
            await page.wait_for_timeout(5000)
            await page.click('a:has-text("Mostrar Mais")')
            await page.wait_for_timeout(5000)
        except Exception as erro:
            print("Erro ao preencher formulario de CEP", erro)

        # Extraindo a qtd de items que tem na pagina
        try:
            total_items_page = await page.inner_html('xpath=//*[@id="gatsby-focus-wrapper"]/div/div[4]/div[1]/div[3]/div/div[2]/div[3]/span')
        except Exception as erro:
            print("Erro ao extrair total de items da página", erro)

        # Extraindo e formatando os dados da pagina
        try:
            for item in range(1, int(total_items_page)):
                milk_brand = await page.inner_html(f'#gatsby-focus-wrapper > div > div:nth-child(4) > div.css-v5flj2 > div.css-2imjyh > div > div.css-15rvxfd > div:nth-child({item}) > a > h3')

                element_old_price = await page.inner_html(f'#gatsby-focus-wrapper > div > div:nth-child(4) > div.css-v5flj2 > div.css-2imjyh > div > div.css-15rvxfd > div:nth-child({item}) > a > div.css-1aun9mh > div.css-1n2fia4 > div.list-price.css-vurnku')
                old_price = element_old_price.split(';')
                if len(old_price) <= 1:
                    formatted_old_price = '0.00'
                else:
                    formatted_old_price = old_price[1].replace(',', '.')

                element_current_price = await page.inner_html(f'#gatsby-focus-wrapper > div > div:nth-child(4) > div.css-v5flj2 > div.css-2imjyh > div > div.css-15rvxfd > div:nth-child({item}) > a > div.css-1aun9mh > div.css-1ntr1be > div')
                current_price = element_current_price.split(';')
                formatted_current_price = current_price[1].replace(',', '.')

                element_link = await page.inner_html(f'#gatsby-focus-wrapper > div > div:nth-child(4) > div.css-v5flj2 > div.css-2imjyh > div > div.css-15rvxfd > div:nth-child({item})')
                product_link = element_link.split()
                formatted_product_link = product_link[3].split('"')

                # Inserindo os dados coletados em um array
                milk_list.append({
                    'Marca': milk_brand.upper(),
                    'Preço Antigo': formatted_old_price,
                    'Preço Atual': formatted_current_price,
                    'Link': f'https://mercado.carrefour.com.br{formatted_product_link[1]}'
                })
            # print(milk_list) # TODO: Parei aqui... falta pegar o valor do usuario p/ comparar com os valores extraidos do site
            # Passando os dados extraídos para a classe de processamento dos dados
            processing.data_processing(milk_list)
        except Exception as erro:
            print("Erro ao extrair item da página: ", erro)

        # Fechando o navegador
        await browser.close()

    async def main():
        async with async_playwright() as playwright:
            await run(playwright)

    asyncio.run(main())

    time.sleep(300)
