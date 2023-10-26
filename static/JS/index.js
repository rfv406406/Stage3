// function getData(){
//     fetch("/api/attractions?page=0")
//     .then(function(response){
//         return response.json();
//     })
//     .then(function(data){

//         let frame4Items = document.querySelectorAll(".frame4-item");
        
//         for(let i = 0; i < data.data.length; i++){
            
//             let imageURL = data.data[i].images;
//             let nameData = data.data[i].name;
//             let mrtData = data.data[i].mrt;
//             let categoryData = data.data[i].category;
//             let idData = data.data[i].id;

//             let frame4ItemImgContainer = frame4Items[i].querySelector(".frame4-item-img");
//             let frame4ItemName = frame4Items[i].querySelector(".frame4-item-name");
//             let frame4ItemMrt = frame4Items[i].querySelector(".frame4-item2-mrt");
//             let frame4ItemCategory = frame4Items[i].querySelector(".frame4-item2-category");

//             // 设置数据
//             frame4ItemName.textContent = nameData;
//             frame4ItemMrt.textContent = mrtData;
//             frame4ItemCategory.textContent = categoryData;
        
//             let image = document.createElement("img");
//             image.src = imageURL[0];
//             frame4ItemImgContainer.appendChild(image);

//             frame4Items[i].addEventListener("click", function(event) {
//                 event.preventDefault();
//                 console.log(idData);
//                 window.location = "/attraction/" + idData;
//                     })
//                 }})  
//             }
// getData();

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
    console.log(formData)
    
    try{
        const response = await fetchData(formData);
        const data = await handleResponse(response);
        console.log(data);
    }catch(error){
        handleError(error);
    }
}

async function fetchData(formData){
    const response = fetch("/api/getmessage", {
        method: 'POST',
        body: formData,
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


