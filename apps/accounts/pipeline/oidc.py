#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from ..models import UserProfile
from jwkest.jwt import JWT
import json

__author__ = "Alan Viars"


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'verifymyidentity-openidconnect':

        profile, g_o_c = UserProfile.objects.get_or_create(user=user)

        if 'id_token' in response.keys():
            id_token = response.get('id_token')
            parsed_id_token = JWT().unpack(id_token)
            payload = parsed_id_token.payload()
            if 'given_name' in payload:
                profile.user.first_name = payload['given_name']
                
            if 'family_name' in payload:
                profile.user.last_name = payload['family_name']          
            
            if 'sub' in payload:
                profile.subject = payload['sub']

            if 'nickname' in payload:
                profile.nickname = payload['nickname']

            if 'phone_number' in payload:
                profile.mobile_phone_number = payload['phone_number']

            if 'birthdate' in payload:
                if payload['birthdate'] not in ("None", ""):
                    profile.birth_date = payload['birthdate']

            if 'gender' in payload:
                profile.gender = payload['gender']

            if 'email_verified' in payload:
                profile.email_verified = payload['email_verified']

            if 'gender_identity' in payload:
                profile.gender_identity = payload['gender_identity']

            if 'middle_name' in payload:
                profile.middle_name = payload['middle_name']

            if 'phone_verified' in payload:
                profile.phone_verified = payload['phone_verified']

            if 'ial' in payload:
                profile.identity_assurance_level = payload['ial']

            if ('picture' in payload and 'None' not in payload['picture']
                    and 'no-img' not in payload['picture']):
                profile.picture_url = payload['picture']

            profile.most_recent_id_token_payload = json.dumps(
                payload, indent=4)

        profile.user.save()
        profile.save()
