## **Как да инсталираме Logic Crusher?**
1. **Сваляме съдържанието от конкретното `repository`.**
2. **Отваряме папката `source`, след което стартираме команден прозорец в тази директория.**

<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot1.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot2.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot3.png" alt="Image 1" width="1000"/>
</div>
<br><br>

3. **Копираме и поставяме командата от `command.txt` в командния прозорец.**
    - **Забележка:** командата в `command.txt` е примерна. Нужно е ръчно да се актуализира пътят към папката source, така че да съответства на реалното ѝ местоположение на вашия компютър.

4. **Изчакваме PyInstaller да приключи. Ако всичко е протекло нормално, трябва да се появят папките build, dist и файлът main.spec. Изпълнимият файл на         
    приложението се намира в папка dist.**
- **Забележки:**
    - Иконата на приложението представлява `.ico файл`, който е комбинация от изображения с размери `256x256`, `128x128`, `64x64`, `32x32` и `16x16` пиксела. В 
      някои случаи (особено ако операционната система или файловият мениджър не разпознават тези размери) изображението може да не бъде показано коректно.
    - При първо използване на `Visualisation of AST` или `Generate Circuit` се създават допълнителни файлове в папката source, които пазят информация за последно         преизчисления булев израз. При всяко следващо използване тези файлове се презаписват.
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot4.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot5.png" alt="Image 1" width="1000"/>
</div>
<br><br>
<br><br>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="screenshots/screenshot6.png" alt="Image 1" width="1000"/>
</div>
<br><br>
