import os
import openai
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import gridfs
import torch
import open_clip
from PIL import Image
from django.http import HttpResponse
from django.utils import timezone
from pymongo import MongoClient
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from django.shortcuts import render, get_object_or_404, redirect
from myproject import settings
from ..forms import *
from ..models import *
from ..clip_model import *
from googletrans import Translator
import base64
import time

from django.forms.models import modelformset_factory
from django.contrib.auth.models import User

# Create your views here.
def viewDiary(request):
    return render(request, 'diaryapp/diary.html')

load_dotenv()
# openai.api_key ="${OPEN_API_KEY}"

def image_detail(request, pk):
    image_model = ImageModel.objects.get(pk=pk)
    image_data = base64.b64decode(image_model.image_file)
    return HttpResponse(image_data, content_type="image/png")

def generate_dynamic_descriptions():
    descriptions = [
        "dog", "park", "cat", "sunset", "ocean", "island", 'Village', 'Campsite', 'Lodge', "Safari", "Fountain",
        "street", "landscape", "mountain", "tree", "flow", "friends", "picnic", 'Cottage', "Cruise", "Square",
        "bridge", "sky", "market", "fruits", "vegetables", "Theme park", "Amusement park", "Aquarium", "Plaza",
        "beach", "sea", "coffee", " books", "cafe", "family", " zoo", "Botanical garden", "National park",
        "couple", "castle", "flower", "street", "village", "bridge", "Harbor", "Port", "River", "Waterfall",
        "Promenade", "Viewpoint", "Lighthouse", "Monument", "Memorial", "Statue", "Landmark", "Tower", "Arena",
        "Stadium", "Pasture", "Orchard", "Brewery", "Winery", "Distillery", "Fair", "Carnival", "Parade", "Festival",
        "Hiking trail", "Bike trail", "Ski slope", "Golf course"
    ]
    return descriptions

# 번역 API
def translate_to_korean(text): # 일기 내용 한국어로 번역
    translator = Translator()
    translated = translator.translate(text, src='en', dest='ko')
    return translated.text
# def translate_to_English(text): # 입력한 감정,장소 영어로 번역
#     translator = Translator()
#     translated = translator.translate(text, src='ko', dest='en')
#     return translated.text

# GPT2 API사용해서 일기 가져오는 부분
#@login_required
# def generate_diary(request):
#     if request.method == 'POST':
#         #writer = request.user
#         form = DiaryForm(request.POST, request.FILES)
#         image_form = ImageUploadForm(request.POST, request.FILES)
#
#         if form.is_valid() and image_form.is_valid():
#             diarytitle = form.cleaned_data['diarytitle']
#             place = form.cleaned_data['place']
#             emotion = form.cleaned_data['emotion']
#             withfriend = form.cleaned_data['withfriend']
#             content = form.cleaned_data['content']
#             representative_image = request.FILES.get('image_file')
#             user_email = settings.DEFAULT_FROM_EMAIL # user생기면 user_email없애고 상단의 writer 사용
#
#             # place 번역
#             translated_place = translate_to_English(place)
#
#             # CLIP 모델과 전처리기 로드
#             model_info = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
#             # print(model_info)  # 반환 값을 확인하기 위해 출력
#
#             # 적절한 반환 값을 사용하도록 수정
#             clip_model = model_info[0]
#             preprocess = model_info[1]
#
#             image = Image.open(representative_image)
#             image = preprocess(image).unsqueeze(0)
#
#             # 이미지 설명 후보 생성
#             descriptions = generate_dynamic_descriptions()
#
#             # 설명 후보들을 CLIP 모델로 처리
#             tokens = open_clip.tokenize(descriptions)
#             with torch.no_grad():
#                 image_features = clip_model.encode_image(image)
#                 text_features = clip_model.encode_text(tokens)
#                 similarity = torch.softmax((100.0 * image_features @ text_features.T), dim=-1)
#                 best_description_idx = similarity.argmax().item()
#                 best_description = descriptions[best_description_idx]
#
#             prompt = (
#                 f"Please draft my travel diary based on this information. 'I recently visited {translated_place} in korea and i felt a strong sense of {emotion}. One of the notable experiences was {best_description}.' ")
#             # GPT-2 모델을 사용하여 텍스트 생성
#             model_name = "gpt2"
#             model = GPT2LMHeadModel.from_pretrained(model_name)
#             tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#             inputs = tokenizer.encode(prompt, return_tensors='pt')
#             outputs = model.generate(inputs, max_length=1000, num_return_sequences=1, no_repeat_ngram_size=2,
#                                      early_stopping=True)
#
#             diary_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#
#             # 프롬프트 내용 제외
#             diary_text_parts = diary_text.split(prompt)
#             if len(diary_text_parts) > 1:
#                 extracted_content = diary_text_parts[1].strip()
#             else:
#                 extracted_content = diary_text.strip()
#
#             translated_text = translate_to_korean(extracted_content)
#
#             # 일기 저장
#             unique_diary_id = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{diarytitle}"
#             diary_entry = AiwriteModel.objects.create(
#                 unique_diary_id=unique_diary_id,
#                 user_email=user_email,
#                 diarytitle=diarytitle,
#                 place=place,
#                 #emotion=translated_emotion,
#                 withfriend=withfriend,
#                 content=translated_text,
#             )
#             diary_entry.save()
#
#             # # 태그 처리
#             # tags = form.cleaned_data['tags']
#             # for tag in tags:
#             #     diary_entry.tags.add(tag)
#
#             # 대표 이미지 처리
#             if representative_image:
#                 image_model = ImageModel(is_representative=True)
#                 image_model.save_image(Image.open(representative_image))
#                 image_model.save()
#                 diary_entry.representative_image = image_model
#                 diary_entry.save()
#
#                 # 추가 이미지 처리
#             images = request.FILES.getlist('images')
#             for img in images:
#                 additional_image_model = ImageModel(is_representative=False)
#                 additional_image_model.save_image(Image.open(img))
#                 additional_image_model.save()
#                 diary_entry.images.add(additional_image_model)  # ManyToMany 관계 설정
#
#             return redirect('list_diary', permanent=True)
#         else:
#             return render(request, 'diaryapp/list_diary.html', {'form': form, 'image_form': image_form})
#     else:
#         form = DiaryForm()
#         image_form = ImageUploadForm()
#
#     return render(request, 'diaryapp/write_diary.html', {'form': form, 'image_form': image_form})

"""GPT3로 일기 생성"""
def generate_diary(request):
    if request.method == 'POST':
        start_time = time.time()
        form = DiaryForm(request.POST, request.FILES)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            diarytitle = form.cleaned_data['diarytitle']
            place = form.cleaned_data['place']
            emotion = form.cleaned_data['emotion']
            withfriend = form.cleaned_data['withfriend']
            representative_image = request.FILES.get('image_file')

            user_email = settings.DEFAULT_FROM_EMAIL
            # user_email = request.user.email

            # place 번역
            #translated_place = translate_to_English(place)

            # # CLIP 모델과 전처리기 로드
            # model_info = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
            #
            # # 적절한 반환 값을 사용하도록 수정
            # clip_model = model_info[0]
            # preprocess = model_info[1]

            image = Image.open(representative_image)
            image = preprocess(image).unsqueeze(0)

            CLIP_start_time = time.time()
            # 이미지 설명 후보 생성
            descriptions = generate_dynamic_descriptions()

            # 설명 후보들을 CLIP 모델로 처리
            tokens = open_clip.tokenize(descriptions)
            with torch.no_grad():
                image_features = clip_model.encode_image(image)
                text_features = clip_model.encode_text(tokens)
                similarity = torch.softmax((100.0 * image_features @ text_features.T), dim=-1)
                best_description_idx = similarity.argmax().item()
                best_description = descriptions[best_description_idx]
            CLIP_end_time = time.time()
            print('------------- CLIP image --------', CLIP_end_time - CLIP_start_time)

            GPT_start_time = time.time()
            prompt = (
                f"Please draft my travel diary based on this information. "
                f"I recently visited {place} in korea and I felt a strong sense of {emotion}. "
                f"One of the notable experiences was {best_description}.I want answers in Korean. I hope it's about 5sentences long")

            # GPT-3.5 모델을 사용하여 다이어리 생성
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=1
            )
            GPT3content = completion['choices'][0]['message']['content']
            GPT_end_time = time.time()
            print('------------- gpt image --------', GPT_end_time - GPT_start_time)

            # emotion 번역
            translated_emotion = translate_to_korean(emotion)

            # 일기 저장
            unique_diary_id = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{diarytitle}"
            diary_entry = AiwriteModel.objects.create(
                unique_diary_id=unique_diary_id,
                user_email=user_email,
                diarytitle=diarytitle,
                place=place,
                emotion=translated_emotion,
                withfriend=withfriend,
                content=GPT3content,
            )
            diary_entry.save()

            image_start_time = time.time()

            # 추가 이미지 처리
            images = request.FILES.getlist('images')
            for img in images:
                additional_image_model = ImageModel(is_representative=False)
                additional_image_model.save_image(Image.open(img))
                additional_image_model.save()
                diary_entry.images.add(additional_image_model)  # ManyToMany 관계 설정

            # 대표 이미지 처리
            if representative_image:
                image_model = ImageModel(is_representative=True)
                image_model.save_image(Image.open(representative_image))
                image_model.save()
                diary_entry.representative_image = image_model
                diary_entry.save()

            # # 추가 이미지 처리
            # images = request.FILES.getlist('images')
            # for img in images:
            #     additional_image_model = ImageModel(is_representative=False)
            #     additional_image_model.save_image(Image.open(img))
            #     additional_image_model.save()
            #     diary_entry.images.add(additional_image_model)  # ManyToMany 관계 설정
            image_end_time = time.time()
            print('------------- get image --------', image_end_time - image_start_time)
            end_time = time.time()
            print('------------- total end --------', end_time - start_time)
            return redirect(reverse('detail_diary_by_id', kwargs={'unique_diary_id': unique_diary_id}))
        else:
            return render(request, 'diaryapp/list_diary.html', {'form': form, 'image_form': image_form})

    else:
        form = DiaryForm()
        image_form = ImageUploadForm()

    return render(request, 'diaryapp/write_diary.html', {'form': form, 'image_form': image_form})


# 직접 일기 부분 작성
"""사용자가 일기 작성"""
def write_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            diarytitle = form.cleaned_data['diarytitle']
            place = form.cleaned_data['place']
            withfriend = form.cleaned_data['withfriend']
            content = form.cleaned_data['content']

            # user_email = request.user.email
            user_email = settings.DEFAULT_FROM_EMAIL

            # # 친구 태그 파싱
            # friend_nicknames = request.POST.get('friends', '').split(',')
            # friends = []
            # # 친구태그
            # for nickname in friend_nicknames:
            #     if nickname.startswith('@'):
            #         nickname = nickname[1:].strip()  # @제거하고 닉네임만 인식
            #         # DB에서 해당 닉네임 사용자 검색 - users_collection위치에 몽고DB 유저모델로 생성된 컬렉션 위치
            #         user_data = users_collection.find_one({'username': nickname})
            #         if user_data:
            #             user = User.objects.get(username=user_data['username'])
            #             friends.append(user)

            # 일기 저장
            unique_diary_id = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{diarytitle}"
            diary_entry = AiwriteModel.objects.create(  # 저장되는 다이어리
                unique_diary_id=unique_diary_id,
                user_email=user_email,
                diarytitle=diarytitle,
                place=place,
                withfriend=withfriend,
                # friends=friends,
                content=content,
            )
            diary_entry.save()

            # # 태그 처리
            # tags = form.cleaned_data['tags']
            # for tag in tags:
            #     diary_entry.tags.add(tag)

            # 대표 이미지 처리
            representative_image = request.FILES.get('image_file')
            if representative_image:
                image_model = ImageModel(is_representative=True)
                image_model.save_image(Image.open(representative_image))
                image_model.save()
                diary_entry.representative_image = image_model
                diary_entry.save()

            # 추가 이미지 처리
            images = request.FILES.getlist('images')
            for img in images:
                additional_image_model = ImageModel(is_representative=False)
                additional_image_model.save_image(Image.open(img))
                additional_image_model.save()
                diary_entry.images.add(additional_image_model)  # ManyToMany 관계 설정

            return redirect(reverse('detail_diary_by_id', kwargs={'unique_diary_id': unique_diary_id}))
        else:
            return render(request, 'diaryapp/write_diary.html', {'form': form, 'image_form': image_form})
    else:
        form = DiaryForm()
        image_form = ImageUploadForm()

    return render(request, 'diaryapp/write_diary.html', {'form': form, 'image_form': image_form})

'''태그된 다른 사용자의 메인 다이어리로 이동 - 메인화면 html주소 변동 필요'''
# def user_diary_main(request, username):
#     user = get_object_or_404(User, username=username)
#     diary_entries = AiwriteModel.objects.filter(tags__name__startswith='@', tags__name=username)
#     return render(request, 'user_diary_main.html', {'user': user, 'diary_entries': diary_entries})

'''전체 일기 리스트 - 유저 인증이 필요 없을 듯'''
def list_diary(request):
    diary_list = AiwriteModel.objects.all().order_by('-created_at')
    return render(request, 'diaryapp/list_diary.html', {'diary_list': diary_list})

'''로그인한 사용자 확인 가능한 본인 일기 리스트'''
# @login_required
# def list_user_diary(request):
#     user = request.user
#     diary_list = AiwriteModel.objects.filter(writer=user).order_by('-created_at')
#     return render(request, 'diaryapp/user_list_diary.html', {'diary_list': diary_list})

# 태그된 다이어리까지 전부 가져오기
# @login_required
# def tag_list_user_diary(request):
#     user = request.user
#     write_diary = AiwriteModel.objects.filter(writer=user).order_by('-created_at')
#     tag_diary = AiwriteModel.objects.filter(tags__name__startswith='@').filter(tags__name__in=[tag.name for tag in user.tags.all()]).exclude(writer=user).order_by('-created_at')
#
#
#     # 쓴 다이어리, 태그한 다이어리 따로 불러오기
#     # context = {
#     #     'write_diary': write_diary,
#     #     'tag_diary': tag_diary
#     # }
#
#     # 쓴 다이어리, 태그한 다이어리 합쳐서 시간 순으로 불러오기
#     diary = (write_diary | tag_diary).order_by('-created_at')
#     context = {
#         'diary' : diary
#     }
#     return render(request, 'diaryapp/user_list_diary.html', context)

'''일기 내용 확인'''
def detail_diary_by_id(request, unique_diary_id):
    # user_email = request.user.email
    user_email = settings.DEFAULT_FROM_EMAIL
    diary = get_object_or_404(AiwriteModel, unique_diary_id=unique_diary_id)
    form = CommentForm()
    # tagged_users = diary.get_tagged_users()
    # return render(request, 'diaryapp/detail_diary.html', {'diary': diary, 'tagged_users': tagged_users})
    return render(request, 'diaryapp/detail_diary.html', {'diary': diary,'form': form})

'''다이어리 여행일정 모달 창'''
def plan_modal(request, unique_diary_id):
    diary = get_object_or_404(AiwriteModel, unique_diary_id=unique_diary_id)
    return render(request,  'diaryapp/plan_modal.html', {'diary': diary})


'''
user가 생기면 변경 - 로그인한 사용자를 기준으로 본인의 일기와 다른 사용자의 일기를 볼 때 화면이 다름
'''
# @login_required
# def detail_diary_by_id(request, unique_diary_id):
#     user = request.user
#     diary = get_object_or_404(AiwriteModel, unique_diary_id=unique_diary_id)
#     # tagged = diary.get_tagged_users()
#     # comments = diary.comments.all()
#     if diary.writer == user:
#         template = 'diaryapp/detail_diary.html'
#     else:
#         template = 'diaryapp/detail_diary_otheruser.html'
#     context = {
#         'diary':diary,
#         # 'tagged':tagged,
#         # 'comments':comments
#     }
#     return render(request, template, context)

'''일기 내용 업데이트'''
# @login_required # html에서 할 수 있으면 삭제
def update_diary(request, unique_diary_id):
    diary = get_object_or_404(AiwriteModel, unique_diary_id=unique_diary_id)

    if request.method == 'POST':

        # emotion 번역
        diary.diarytitle = request.POST['diarytitle']
        diary.place = request.POST['place']
        diary.withfriend = request.POST['withfriend']
        diary.content = request.POST['content']

        # user_email = request.user.email
        # from django.contrib.auth import authenticate, login
        # user = authenticate(request, username=username)
        user_email = settings.DEFAULT_FROM_EMAIL
        diary.save()

        # 대표 이미지 처리 (대표 이미지 변경)
        representative_image = request.FILES.get('image_file')
        if representative_image:
            if diary.representative_image:
                diary.representative_image.delete()  # 기존 대표 이미지 삭제
            image_model = ImageModel(is_representative=True)
            image_model.save_image(Image.open(representative_image))
            image_model.save()
            diary.representative_image = image_model
            diary.save()

        # 추가 이미지 처리
        images = request.FILES.getlist('images')
        for img in images:
            additional_image_model = ImageModel(is_representative=False)
            additional_image_model.save_image(Image.open(img))
            additional_image_model.save()
            diary.images.add(additional_image_model)  # ManyToMany 관계 설정

        # 기존 이미지 삭제 처리
        delete_image_ids = request.POST.getlist('delete_images')
        for image_id in delete_image_ids:
            image_to_delete = ImageModel.objects.get(id=image_id)
            diary.images.remove(image_to_delete)
            image_to_delete.delete()

        return redirect(reverse('detail_diary_by_id', kwargs={'unique_diary_id': unique_diary_id}))
    else:
        form = DiaryForm(instance=diary)
        image_form = ImageUploadForm()

    existing_images = diary.images.all()

    return render(request, 'diaryapp/update_diary.html', {
        'diary': diary,
        'existing_images': existing_images,
        'form': form,
        'image_form': image_form,
    })

'''일기 내용 삭제'''
# @login_required   # html에서 할 수 있으면 삭제
def delete_diary(request, unique_diary_id):
    # user_email = request.user.email
    user_email = settings.DEFAULT_FROM_EMAIL
    diary = get_object_or_404(AiwriteModel, unique_diary_id=unique_diary_id)
    if request.method == 'POST':
        diary.delete()
        return redirect('list_diary')
    return redirect('list_diary')