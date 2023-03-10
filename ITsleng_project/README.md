# Навык Яндекс.Алиса "IT Sleng"  

#### Общее описание: 

Навык "IT сленг" реализован в виде интерактивной игры-викторины, где пользователь отвечает на вопросы с вариантами ответов или угадывает пропущенные слова из мира IT диалекта, а также англицизмы других связанных сфер.
За каждый верный ответ, разгаданный с первой попытки, начисляются 2 балла, со второй – 1 балл, за неверный ответ –  0 баллов. Игрок может узнать как свой общий рейтинг, так и за текущую игру.
Доступны возможность по команде узнать правила, вызвать помощь, пропустить вопрос, сдаться.

Общение с пользователем и ведение по сценарию в ходе игры рассчитан на "бесповерхностное" взаимодействие. При этом на экране реализованы suggest-кнопки и дополнительная информация.

#### Функционал: 
 Стек: Python/Django
 
 *Имплементировано:*
- ведение профайлов для каждого пользователя/сессии ( `.json` + библиотека `rapidjson`);
- система рейтинга за всю историю посещения и за сессию;
- применение интентов и NLP от Яндекса, реакция на нецензурную лексику и др.;
- настройка и сбор *AppMetrica* по событиям (см. Event Map);

На данный момент проект дорабатывается для финального деплоя.

*В процессе реализации:*
- применение асинхронной обработки http-запросов;
- покрытие кода тестами;
- периодическая очистка старых файлов сессий с помощью `apscheduler` ;
- общий рефакторинг кода (PEP8, типизация, модульность и пр.);
- расширение БД вопросов-ответов-пояснений;
- создания контекстных менеджеров для обновления`.json`;

