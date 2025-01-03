// pull dates from pitems.json
let images = [
    {
        "filename": "commission.jpg",
        "portrait_name": "Anonymous",
        "date": "2024-04-28"
    },
    {
        "filename": "tim.jpg",
        "portrait_name": "Tim",
        "date": "2024-05-06",
    },
    {
        "filename": "mom.jpg",
        "portrait_name": "Mom",
        "date": "2024-05-04",
    },
    {
        "filename": "aaron-frazer.jpg",
        "portrait_name": "Aaron Frazer - Love Is What You Make It",
        "date": "2022-08-17",
    },
    {
        "filename": "bill-withers.jpeg",
        "portrait_name": "Bill Withers",
        "date": "2019-09-26",
    },
    {
        "filename": "charlie.png",
        "portrait_name": "Charlie Puth",
        "date": "2023-02-26",
    },
    {
        "filename": "jill.png",
        "portrait_name": "Jill Conway",
        "date": "2017-05-03",
    },
    {
        "filename": "john-jordan.png",
        "portrait_name": "John & Jordan",
        "date": "2023-03-14",
    },
    {
        "filename": "jorja.jpeg",
        "portrait_name": "Jorja Smith",
        "date": "2021-04-17"
    },
    {
        "filename": "lane.JPG",
        "portrait_name": "Lane",
        "date": "2016-08-28"
    },
    {
        "filename": "mahalia.png",
        "portrait_name": "Mahalia",
        "date": "2022-10-21"
    },
    {
        "filename": "moe.jpeg",
        "portrait_name": "Moe",
        "date": "2021-12-22"
    },
    {
        "filename": "presley.JPG",
        "portrait_name": "Presley",
        "date": "2017-09-02",
    },
    {
        "filename": "sarahfinal.JPG",
        "portrait_name": "Sarah",
        "date": "2018-02-26",
    },
    {
        "filename": "sinead-harnett.jpeg",
        "portrait_name": "Sinead Harnett",
        "date": "2020-11-23",
    },
    {
        "filename": "therese-curatolo.jpeg",
        "portrait_name": "Therese Curatolo",
        "date": "2020-04-01",
    },
    {
        "filename": "wednesday.jpg",
        "portrait_name": "Wednesday",
        "date": "2023-01-30",
    },
    {
        "filename": "bernie.jpeg",
        "portrait_name": "Bernie",
        "date": "2020-01-25",
    },
    {
        "filename": "boburnham.JPG",
        "portrait_name": "Bo Burnham",
        "date": "2021-07-24",
    },
    {
        "filename": "don-draper.jpeg",
        "portrait_name": "Don Draper",
        "date": "2019-07-29",
    },
    {
        "filename": "johncommission.JPG",
        "portrait_name": "John",
        "date": "2017-01-15",
    },
    {
        "filename": "jolie.jpeg",
        "portrait_name": "Jolie",
        "date": "2021-04-21",
    },
    {
        "filename": "kevin.JPG",
        "portrait_name": "Kevin",
        "date": "2016-11-09",
    },
    {
        "filename": "laufey.png",
        "portrait_name": "Laufey",
        "date": "2022-10-20",
    },
    {
        "filename": "masego.JPG",
        "portrait_name": "Masego",
        "date": "2018-02-07",
    },
    {
        "filename": "ongo.jpeg",
        "portrait_name": "Ongo",
        "date": "2019-05-23",
    },
    {
        "filename": "Saba.JPG",
        "portrait_name": "Saba",
        "date": "2021-12-05",
    },
    {
        "filename": "vienna.JPG",
        "portrait_name": "Vienna",
        "date": "2016-12-26",
    },
    {
        "portrait_name": "Collection",
        filename: "collection.jpg",
        date: "2023-02-20"
    },
    {
        "portrait_name": "Commission",
        filename: "dog-commission-2.jpg",
        date: "2024-12-23"
    },
    {
        portrait_name: "Commission",
        filename: "dog-commission-0.jpg",
        date: "2024-12-17"
    },
    {
        portrait_name: "Commission",
        filename: "dog-commission-1.jpg",
        date: "2024-12-23",
    },
    {
        portrait_name: "Commission",
        filename: "dog-commission-3.jpg",
        date: "2024-12-16",
    },
    {
        portrait_name: "Hunt Family",
        filename: "hunt-family.jpg",
        date: "2024-06-15"
    },
    {
        portrait_name: "Post Malone WIP 1",
        filename: "post-malone-0.jpg",
        date: "2024-11-15"
    },
    {
        portrait_name: "Post Malone WIP 2",
        filename: "post-malone-1.jpg",
        date: "2024-11-15"
    },
    {
        portrait_name: "Post Malone WIP 3",
        filename: "post-malone-2.jpg",
        date: "2024-11-16"
    },
    {
        portrait_name: "Post Malone Final",
        filename: "post-malone-3.jpg",
        date: "2024-11-16"
    },
    {
        portrait_name: "Sam Altman WIP 1",
        filename: "sam-altman-1.jpg",
        date: "2024-11-17"
    },
    {
        portrait_name: "Sam Altman Final",
        filename: "sam-altman-2.jpg",
        date: "2024-11-18"
    },

    {
        portrait_name: "Taylor Tomlinson WIP 1",
        filename: "taylor-tomlinson-0.jpg",
        date: "2024-11-18"
    },
    {
        portrait_name: "Taylor Tomlinson WIP 2",
        filename: "taylor-tomlinson-1.jpg",
        date: "2024-12-24"
    },
    {
        portrait_name: "Taylor Tomlinson WIP 3",
        filename: "taylor-tomlinson-2.jpg",
        date: "2024-12-26"
    },
    {
        portrait_name: "Taylor Tomlinson Final",
        filename: "taylor-tomlinson-3.jpg",
        date: "2024-12-27"
    },
]
let mostRecent = [];

// sort in reverse chronological order
const sortedPortfolio = images.sort((a, b) => new Date(b.date) - new Date(a.date))

const MOST_RECENT_COUNT = 6;
for (let i = 0; i < MOST_RECENT_COUNT; i++) {
    mostRecent.push(sortedPortfolio[i]);
}

const createGridItemForImage = (image) => {
    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item');
    const imgBox = document.createElement('div');
    imgBox.classList.add('img-box');
    const img = document.createElement('img');
    img.src = `/img/${image.filename}`;
    img.alt = image.portrait_name;
    imgBox.appendChild(img);
    // add name 
    const description = document.createElement('p');
    description.innerText = `${image.portrait_name}, ${new Date(image.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`;
    imgBox.appendChild(description);

    // wrap in a link to the image

    const link = document.createElement('a');
    link.href = `/img/${image.filename}`;
    link.appendChild(imgBox);
    gridItem.appendChild(link);
    return gridItem;
}

const mostRecentGrid = document.querySelector('.portfolio-grid.most-recent');
if (mostRecentGrid) {
    mostRecent.forEach((image, index) => {
        const gridItem = createGridItemForImage(image);
        mostRecentGrid.appendChild(gridItem);
    });
}

const fullPortfolioGrid = document.querySelector('.portfolio-grid.full');
if (fullPortfolioGrid) {
    sortedPortfolio.forEach((image) => {
        const gridItem = createGridItemForImage(image);
        fullPortfolioGrid.appendChild(gridItem);
    });
}