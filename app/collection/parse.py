import logging
import traceback
import sys
import bs4
import json
from selenium import webdriver

from config.config import SHARDNET_LINK, MAINNET_LINK


########################################################################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='[%(asctime)s]:[%(levelname)s]:[%(filename)s]:[%(lineno)d]: %(message)s',
    )


########################################################################################################################
def parse_near() -> str:
    browser = webdriver.Firefox(
        executable_path=r'G:\Утилиты\Pytnon\Education\selenium_traning\geckodriver\geckodriver.exe',
    )
    pgs_links = {7: SHARDNET_LINK, 3: MAINNET_LINK}
    result_data = {'shardnet': [], 'mainnet': []}

    for pgs, link in pgs_links.items():
        pg = 1
        browser.get(link)

        for page in range(pgs):
            pg += 1
            logger.info(f'{page} - start')
            main_page = browser.page_source
            soup = bs4.BeautifulSoup(main_page, features="lxml")
            search_results = soup.find_all(
                class_='c-TableRowWrapper-jUPfkR mx-0'
            )

            for n, result in enumerate(search_results, start=1):
                if n > 3:
                    n += 1
                try:
                    position = result.find(
                        class_="c-OrderTableCell-clytRC"
                    ).text
                    status = result.find(
                        class_="c-ValidatingLabelWrapper-eennLm c-ValidatingLabelWrapper-eennLm-fFWhBO-type-active badge"
                    ).text
                    total = result.find(
                        class_="c-ValidatorNodesText-hdougQ c-StakeText-ePtfAL text-right"
                    ).text

                    fee = soup.select_one(
                        f'div.c-AppWrapper-eIdCBM > div.c-ContentContainer-fGHEql.c-NodesPage-dfbLrd.container-fluid > div.container-fluid > div.c-ValidatorsWrapper-emjxtC.container > div > div > table > tbody > tr:nth-child({n}) > td:nth-child(5)'
                    ).text
                    contr = soup.select_one(
                        f'div.c-AppWrapper-eIdCBM > div.c-ContentContainer-fGHEql.c-NodesPage-dfbLrd.container-fluid > div.container-fluid > div.c-ValidatorsWrapper-emjxtC.container > div > div > table > tbody > tr:nth-child({n}) > td:nth-child(6)'
                    ).text

                    logger.info(f'{page} - find: {position}, {status}, {fee}, {contr}, {total}')
                    validator_data = {
                        'position': position,
                        'status': status,
                        'fee': fee,
                        'contributors': contr,
                        'total': total
                    }
                except Exception as e:
                    logger.error(f'\n{traceback.format_exc()}\n\n')
                else:
                    logger.info(f'\ndata: {validator_data}\n\n')
                    if link == MAINNET_LINK:
                        k = 'mainnet'
                    else:
                        k = 'shardnet'
                    result_data.get(k).append(validator_data)

            if pg > pgs:
                break
            next_page = browser.find_element_by_css_selector(
                f'.c-PaginateWrapper-bBXXIO > li:nth-child({3 if pg == 2 else pg}) > a:nth-child(1)'
            )
            next_page.click()

        filename = 'active_validators.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)
            logger.info(f'{filename} - data well written')
        return filename
