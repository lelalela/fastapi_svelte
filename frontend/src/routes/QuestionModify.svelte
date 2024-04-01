<script>
    import fastapi from "../lib/api";
    import Error from '../components/Error.svelte'
    import {link, push} from 'svelte-spa-router'
    import moment from  'moment/min/moment-with-locales'
    
    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    
    let subject = '';
    let content = '';
    
    let error = {detail:[]}

    function get_question() {
        fastapi('get', `/api/question/detail/${question_id}`, {}, (json) => {
            subject = json.subject
            content = json.content
        })
    }
    get_question();

    function modify_question(event){
        event.preventDefault();
        
        const params = {
            question_id: question_id,
            subject: subject,
            content: content
        }

        fastapi('put', '/api/question/modify', params, 
        (json) => {
            push(`/detail/${question_id}`);
        }, 
        (json_error) => {
            error = json_error
        })

    }


</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click={modify_question} >저장하기</button>
    </form>
</div>