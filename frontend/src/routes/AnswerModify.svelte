<script>
    import fastapi from "../lib/api";
    import Error from '../components/Error.svelte'
    import { push } from 'svelte-spa-router'
    import moment from  'moment/min/moment-with-locales'
    
    moment.locale('ko')

    export let params = {}
    let answer_id = params.answer_id
    let question_id;
    let content = '';
    
    let error = {detail:[]}

    function get_answer() {
        fastapi('get', `/api/answer/detail/${answer_id}`, {}, (json) => {
            content = json.content
            question_id = json.question_id
        })
    }
    get_answer();

    function modify_answer(event){
        event.preventDefault();
        
        console.log(answer_id)

        const params = {
            answer_id: answer_id,
            content: content
        }

        fastapi('put', '/api/answer/modify', params, 
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
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click={modify_answer} >저장하기</button>
    </form>
</div>