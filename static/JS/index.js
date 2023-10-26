fetchData();
async function fetchData() {
    try {
        const response = await getData(); 
        const data = await handleResponse(response);
        console.log(data);
        autoCreateDiv(data);
    } catch(error) {
        handleError(error);
    }
};

const dataSubmit = document.querySelector('#data_submit')
dataSubmit.addEventListener('click', getMessage)

async function getMessage(event){
    event.preventDefault();
    const message = document.querySelector('.message_content').value;
    const fig = document.querySelector('#file').files[0]
    
    // 创建一个 FormData 对象
    let formData = new FormData();
    formData.append('message', message); // 添加消息内容
    formData.append('file', fig); // 添加文件
    // console.log(formData)
    
    try{
        const response = await inputData(formData);
        const data = await handleResponse(response);
        console.log(data);
        await fetchData();
    }catch(error){
        handleError(error);
    }
}

async function inputData(formData){
    const response = fetch("/api/getmessage", {
        method: 'POST',
        body: formData,
    });
    return response;
}

async function getData(){
    const response = fetch("/api/getmessage", {
        method: 'GET',
    });
    return response;
}

async function handleResponse(response) {
    if (!response.ok) {
        throw new Error('Get null from backend');
    }
    return response.json();
}

async function handleError(error) {
    console.error('Backend could got problems', error);
}

function autoCreateDiv(data){
    let main = document.querySelector('.main')
    for(let i =0;i < data.data.length; i++){
        let messages = data.data[i].message;
        let images = data.data[i].URL_image;

        let text = document.createElement('text');
        text.textContent = messages;
        main.appendChild(text);
        if(images){
            let figContainer = document.createElement('div');
            let fig = document.createElement('img')
            fig.src = images;
            figContainer.appendChild(fig)
            main.appendChild(figContainer);
        };

        let separator = document.createElement('div');
        separator.classList.add('separator');
        main.appendChild(separator);
    }
}

