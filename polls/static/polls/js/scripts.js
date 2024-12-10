document.getElementById('logOut').addEventListener('click',
    function () {
        alert('로그아웃 되었습니다.');
    });


document.getElementById('createBoard').addEventListener('click',
    function () {
        alert('보드 생성하기 버튼을 클릭하셨습니다.');
        window.location.href = 'create_board'
    });
